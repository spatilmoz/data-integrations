#!/usr/bin/env python3

from __future__ import division
import time
import json,sys,os,errno,re,argparse
from datetime import datetime
from subprocess import call
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import SalesforceFTP
import Util


def get_date_from_filename(filename):
  m = re.search('DailyEmailSendSummary_(\d+), (\d+), (\d+).csv', filename)
  if m:
    return '-'.join(m.group(1,2,3))
  else:
    raise Exception('unable to parse filename %s' % filename)

def get_date_from_modify(modify_date):
  m = re.search('^(\d{4})(\d{2})(\d{2})', modify_date)
  if m:
    return '-'.join(m.group(1,2,3))
  else:
    raise Exception('unable to parse modify date %s' % modify_date)

def create_dest_dir(dirname):
  full_path = os.path.join(args.dest_dir, dirname)
  if os.path.isdir(full_path):
    logger.info( "Directory exists, not creating: %s" % full_path)
  else:
    logger.info( "Creating: %s" % full_path)
    os.mkdir(full_path)
  return full_path

def download_file( path, filename, date ):
  #date = get_date_from_filename(filename)
  full_dest_path = create_dest_dir(date)

  downloaded_file_and_path = SalesforceFTP.get_file(path, filename, full_dest_path)

if __name__ == "__main__":
 
  parser = argparse.ArgumentParser(description="BrickFTP stuff")
  parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
  parser.add_argument('-l', '--log-level', action='store', help='log level (debug, info, warning, error, or critical)', type=str, default='info')
  parser.add_argument('--dest-dir', action='store', help='destination directory', type=str, default='.')
  parser.add_argument('-a', '--archive', action='store_true', help='move the zip files to the Archive directory after downloading')
  parser.add_argument('--date', action='store', help='the date to retrieve')
  args = parser.parse_args()

  Util.set_up_logging(args.log_level)

  logger = logging.getLogger(__name__)

  logger.info("Starting...")

  path = "/reports"

  files_list = SalesforceFTP.list_files(path=path)
  for filename, facts in files_list:
    print(filename)
    if facts['type'] == 'file' and re.match('DailyEmailSendSummary_', filename):
      print(facts)
      file_date = get_date_from_modify(facts['modify'])
      print(file_date)
      #if args.date and not re.match(args.date, get_date_from_filename(filename)):
      if args.date and args.date != file_date:
        logger.warning( "--date specified, skipping non-date-matching filename: %s date: %s" % (filename,file_date))
        continue
      download_file( path, filename, file_date )
      if args.archive:
        raise(Exception("Unimplemented!"))
        logger.info( "moving file to Archive in SalesforceFTP")
        SalesforceFTP.move_file( file['path'],
                            os.path.join(os.path.dirname(file['path']),
                            'Archive',
                            os.path.basename(file['path'])) )


  logger.info( "Finished.")
