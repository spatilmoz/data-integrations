#!/usr/bin/env python3

import sys,os, argparse
import datetime
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from integrations.connectors import Workday, Util

if __name__ == "__main__":
 
  parser = argparse.ArgumentParser(description="Get Workday data")
  parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
  parser.add_argument('-l', '--log-level', action='store', help='log level (debug, info, warning, error, or critical)', type=str, default='info')
  parser.add_argument('--date', action='store', help='date to retrieve', type=str)
  parser.add_argument('-o', '--output-dir', action='store', help='output directory', type=str, default='./')
  parser.add_argument('-f', '--force', action='store_true', help='run on a date even if it\'s not friday')
  parser.add_argument('-m', '--monthly', action='store_true', help='pull the monthly version of the reports')
  parser.add_argument('--ta-dashboard', action='store_true', help='pull the TA dashboard stuff')
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
    if args.ta_dashboard:
      raise Exception('You can\'t use --monthly with --ta-dashboard')
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

  elif not args.ta_dashboard:
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

  if args.ta_dashboard:
    # the ta_dashabord daily report is a separate special snowflake for the TA Dashboard

    report_type = 'hires'
    logger.info( "Getting %s data" % report_type)
    outfile = os.path.join(args.output_dir, report_type + '_' + str(retrieve_date) + '.csv')

    wd_csv_data = Workday.get_ta_dashboard_data(report_type, str(retrieve_date), start_date)

    logger.info( "Writing %s data to %s" % (report_type, outfile))

    with open(outfile, 'w', encoding="utf-8") as f:
      f.write(wd_csv_data)

  else:
    for report_type in ['headcount', 'hires', 'terminations', 'promotions']:
  
      logger.info( "Getting %s data" % report_type)
      outfile = os.path.join(args.output_dir, report_type + '_' + str(retrieve_date) + '.csv')
  
      wd_csv_data = Workday.get_dashboard_data(report_type, str(retrieve_date), start_date)
  
      logger.info( "Writing %s data to %s" % (report_type, outfile))
  
      with open(outfile, 'w', encoding="utf-8") as f:
        f.write(wd_csv_data)
  
  logger.info( "Finished.")
