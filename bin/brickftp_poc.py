#!/usr/bin/env python3

from __future__ import division
import time
import json,sys,os,errno,re,argparse
from datetime import datetime
from subprocess import call

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import BrickFTP

parser = argparse.ArgumentParser(description="BrickFTP stuff")
parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
parser.add_argument('--dest-dir', action='store', help='destination directory', type=str, default='.')
parser.add_argument('-a', '--archive', action='store_true', help='move the zip files to the Archive directory after downloading')
parser.add_argument('--date', action='store', help='the date to retrieve')
args = parser.parse_args()

debug = args.debug

def print_debug(level, message):
  if debug >= level:
    print("[%s] %s" % (datetime.now(),message))

def get_date_from_sfmc_filename(filename):
  m = re.search('DailySFMC(\d+), (\d+), (\d+).zip', filename)
  if m:
    return '-'.join(m.group(1,2,3))
  else:
    raise Exception('unable to parse filename %s' % filename)

def create_dest_dir(dirname):
  full_path = os.path.join(args.dest_dir, dirname)
  if os.path.isdir(full_path):
    print_debug(3, "Directory exists, not creating: %s" % full_path)
  else:
    print_debug(3, "Creating: %s" % full_path)
    os.mkdir(full_path)
  return full_path

def download_and_extract_file( filename_and_path ):
  date = get_date_from_sfmc_filename(filename_and_path)
  full_dest_path = create_dest_dir(date)

  downloaded_file_and_path = BrickFTP.get_file('/' + filename_and_path, full_dest_path)

  filename_only = os.path.basename(downloaded_file_and_path)
  if re.match('DailySFMC.*zip', filename_only):
    print_debug(3, "Unzipping file")
    call(['unzip', '-qo', filename_only], cwd=full_dest_path)
    print_debug(3, "Removing zip file")
    call(['rm',    filename_only], cwd=full_dest_path)
  else:
    print("Not sure what to make of: %s" % resulting_file_and_path)

if __name__ == "__main__":
 
  print_debug(1, "Starting...")

  BrickFTP.debug(debug)

  files_list = BrickFTP.list_files(path='/etl/Moz_SFDC_Data_Team_Extract')
  for file in files_list:
    if file['type'] == 'file' and re.match('DailySFMC', file['display_name']):
      if args.date and not re.match(args.date, get_date_from_sfmc_filename(file['display_name'])):
        print_debug(3, "--date specified, skipping non-matching filename: %s" % file['display_name'])
        continue
      download_and_extract_file( file['path'] )
      if args.archive:
        print_debug(3, "moving file to Archive in BrickFTP")
        BrickFTP.move_file( file['path'],
                            os.path.join(os.path.dirname(file['path']),
                            'Archive',
                            os.path.basename(file['path'])) )


  print_debug(1, "Finished.")
