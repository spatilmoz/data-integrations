#!/usr/bin/env python3

from __future__ import division
import time
import json,sys,os,errno,re,argparse
from datetime import datetime
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import SalesforceFTP
import Util



def create_dest_dir(dest_dir, dirname):
  full_path = os.path.join(dest_dir, dirname)
  if os.path.isdir(full_path):
    logger.info( "Directory exists, not creating: %s" % full_path)
  else:
    logger.info( "Creating: %s" % full_path)
    os.mkdir(full_path)
  return full_path

def download_file( dest_dir, path, filename, date ):
  #date = get_date_from_filename(filename)
  full_dest_path = create_dest_dir(dest_dir, date)

  downloaded_file_and_path = SalesforceFTP.get_file_stupid_way(path, filename, full_dest_path)

if __name__ == "__main__":
 
  parser = argparse.ArgumentParser(description="SalesforceFTP stuff")
  parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
  parser.add_argument('-l', '--log-level', action='store', help='log level (debug, info, warning, error, or critical)', type=str, default='info')
  parser.add_argument('--dest-dir', action='store', help='destination directory', type=str, default='.')
  parser.add_argument('--filename', action='store', help='filename', type=str, default='15-Day-Email-Send-Summary.csv')
  parser.add_argument('-a', '--archive', action='store_true', help='move the zip files to the Archive directory after downloading')
  parser.add_argument('--date', action='store', help='the date to retrieve')
  args = parser.parse_args()

  Util.set_up_logging(args.log_level)

  logger = logging.getLogger(__name__)

  logger.info("Starting...")

  path = "/reports"

  download_file( args.dest_dir, path, args.filename, args.date )

  logger.info( "Finished.")
