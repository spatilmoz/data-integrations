#!/usr/bin/env python3

import time
import requests
import json,sys,os,errno,re,argparse
import datetime
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import Workday
import Util

if __name__ == "__main__":
 
  parser = argparse.ArgumentParser(description="Sync up XMatters with Workday")
  parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
  parser.add_argument('-l', '--log-level', action='store', help='log level (debug, info, warning, error, or critical)', type=str, default='info')
  parser.add_argument('--date', action='store', help='date to retrieve', type=str)
  parser.add_argument('-o', '--output-dir', action='store', help='output directory', type=str, default='./')
  parser.add_argument('-f', '--force', action='store_true', help='run on a date even if it\'s not friday')
  parser.add_argument('-m', '--monthly', action='store_true', help='pull the monthly version of the reports')
  args = parser.parse_args()
  
  Util.set_up_logging(args.log_level)

  logger = logging.getLogger(__name__)

  logger.info("Starting...")

  if not args.date:
    args.date = datetime.datetime.now().strftime('%Y-%m-%d')

  retrieve_date_l = [ int(i) for i in args.date.split('-') ]
  retrieve_date   = datetime.date(retrieve_date_l[0], retrieve_date_l[1], retrieve_date_l[2])
  start_date      = None
  if args.monthly:
#    if retrieve_date_l[2] != 1 and not args.force:
#      logger.critical( "Specified date (%s) is not the first of the month. Use --force if you're sure" % retrieve_date)
#      exit()
#    first_day  = retrieve_date.replace(day=1)
#    last_month = first_day - datetime.timedelta(days=1)
#    start_date = last_month.strftime("%Y-%m-01")
    # regardless of provided date, set the start_date to the 1st and the retrieve_date to the end
    month = str(retrieve_date_l[1])
    if retrieve_date_l[1] < 10:
      month = '0' + month
    start_date = str(retrieve_date_l[0]) + '-' + month + '-' + '01'
    next_month = retrieve_date.replace(day=28) + datetime.timedelta(days=4)
    retrieve_date = next_month - datetime.timedelta(days=next_month.day)

  else:
    if retrieve_date.isoweekday() != 5 and not args.force:
      logger.critical( "Specified date (%s) is not a Friday. Use --force if you're sure" % retrieve_date)
      exit()

  if not os.path.isdir(args.output_dir):
    logger.critical( "Specified output dir (%s) is not a directory." % args.output_dir)
    exit()

#  if args.output_filename:
#    outfile = os.path.join(args.output_dir, args.output_filename)
#  else:
#    outfile = os.path.join(args.output_dir, 'Employee_Details_Report_' + str(retrieve_date) + '.csv')
#
#  logger.info( "Writing data to %s" % outfile)

  for report_type in ['headcount', 'hires', 'terminations', 'promotions']:

    logger.info( "Getting %s data" % report_type)
    outfile = os.path.join(args.output_dir, report_type + '_' + str(retrieve_date) + '.csv')

    wd_csv_data = Workday.get_dashboard_data(report_type, str(retrieve_date), start_date)

    logger.info( "Writing %s data to %s" % (report_type, outfile))

    with open(outfile, 'w') as f:
      f.write(wd_csv_data.encode('utf-8'))

  logger.info( "Finished.")
