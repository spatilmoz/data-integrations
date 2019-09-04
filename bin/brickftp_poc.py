#!/usr/bin/env python3

from __future__ import division
import sys,os, re,argparse
from subprocess import call
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from integrations.api.connectors import BrickFTP
from integrations.api.connectors import Util


def get_date_from_sfmc_filename(filename):
  m = re.search('DailySFMC(\d+), (\d+), (\d+).zip', filename)
  if m:
    return '-'.join(m.group(1,2,3))
  else:
    raise Exception('unable to parse filename %s' % filename)

def create_dest_dir(dirname):
  full_path = os.path.join(args.dest_dir, dirname)
  if os.path.isdir(full_path):
    logger.info( "Directory exists, not creating: %s" % full_path)
  else:
    logger.info( "Creating: %s" % full_path)
    os.mkdir(full_path)
  return full_path

def download_and_extract_file( filename_and_path ):
  date = get_date_from_sfmc_filename(filename_and_path)
  full_dest_path = create_dest_dir(date)

  downloaded_file_and_path = BrickFTP.get_file('/' + filename_and_path, full_dest_path)

  filename_only = os.path.basename(downloaded_file_and_path)
  if re.match('DailySFMC.*zip', filename_only):
    logger.info( "Unzipping file")
    call(['unzip', '-qo', filename_only], cwd=full_dest_path)
    logger.info( "Removing zip file")
    call(['rm',    filename_only], cwd=full_dest_path)
  else:
    logger.error("Not sure what to make of: %s" % resulting_file_and_path)

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

  files_list = BrickFTP.list_files(path='/etl/Moz_SFDC_Data_Team_Extract')
  for file in files_list:
    if file['type'] == 'file' and re.match('DailySFMC', file['display_name']):
      if args.date and not re.match(args.date, get_date_from_sfmc_filename(file['display_name'])):
        logger.debug( "--date specified, skipping non-matching filename: %s" % file['display_name'])
        continue
      download_and_extract_file( file['path'] )
      if args.archive:
        logger.info( "moving file to Archive in BrickFTP")
        BrickFTP.move_file(file['path'],
                           os.path.join(os.path.dirname(file['path']),
                            'Archive',
                            os.path.basename(file['path'])))


  logger.info( "Finished.")
