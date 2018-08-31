#!/usr/bin/env python3

import time
import requests
import json,sys,os,errno,re,argparse
import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import Workday


def print_debug(level, message):
  if debug >= level:
    print("[%s] %s" % (datetime.datetime.now(),message))

if __name__ == "__main__":
 
  parser = argparse.ArgumentParser(description="Sync up XMatters with Workday")
  parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
  parser.add_argument('--date', action='store', help='date to retrieve', type=str)
  parser.add_argument('-o', '--output-dir', action='store', help='output directory', type=str, default='./')
  parser.add_argument('--output-filename', action='store', help='output filename', type=str)
  parser.add_argument('-f', '--force', action='store_true', help='force changes even if there are a lot')
  args = parser.parse_args()
  
  debug = args.debug

  print_debug(1, "Starting...")

  if not args.date:
    args.date = datetime.datetime.now().strftime('%Y-%m-%d')

  retrieve_date_l = [ int(i) for i in args.date.split('-') ]
  retrieve_date   = datetime.date(retrieve_date_l[0], retrieve_date_l[1], retrieve_date_l[2])
  if retrieve_date.isoweekday() != 5 and not args.force:
    print_debug(1, "Specified date (%s) is not a Friday. Use --force if you're sure" % retrieve_date)
    exit()

  if not os.path.isdir(args.output_dir):
    print_debug(1, "Specified output dir (%s) is not a directory." % args.output_dir)
    exit()

  if args.output_filename:
    outfile = os.path.join(args.output_dir, args.output_filename)
  else:
    outfile = os.path.join(args.output_dir, 'Employee_Details_Report_' + str(retrieve_date) + '.csv')

  print_debug(3, "Writing data to %s" % outfile)

  Workday.debug(debug)

  # get all users from workday
  wd_csv_data = Workday.get_dashboard_data(str(retrieve_date))

  with open(outfile, 'w') as f:
    f.write(wd_csv_data)

  print_debug(1, "Finished.")
