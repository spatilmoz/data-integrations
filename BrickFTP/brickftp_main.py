import time
import requests
import json,sys,os,errno,re
from secrets_brickftp import config as brickftp_config
from datetime import datetime
import logging

class LocalConfig(object):
  def __init__(self):
    self.api_url  = 'https://mozilla.brickftp.com/api/rest/v1/'
    self.debug    = 3

  def __getattr__(self, attr):
    return brickftp_config[attr]

_config = LocalConfig()

def list_files(path='/'):
  # Returns an array like:
  # [
  #   {
  #     u'display_name': u'DailySFMC2018, 06, 29.zip',
  #     u'region': u'us-east-1',
  #     u'provided_mtime': u'2018-06-29T07:08:07+00:00',
  #     u'mtime': u'2018-06-29T07:08:08+00:00',
  #     u'crc32': u'3f68b6a6',
  #     u'path': u'etl/Moz_SFDC_Data_Team_Extract/DailySFMC2018, 06, 29.zip',
  #     u'permissions': u'rwd',
  #     u'md5': u'5b57fc2db48b0c860d6803b171819cc4',
  #     u'type': u'file',
  #     u'id': 1182667528, u'size': 24953177
  #   },
  #   {
  #     u'display_name': u'DailySFMC2018, 06, 28.zip',
  #     u'region': u'us-east-1',
  #            [...]
  #   }
  # ]
  #
  logging.info( "Listing files for path: %s" % path)
  brickftp_url = _config.api_url + '/folders/' + path
  response = requests.get(brickftp_url, auth=(_config.api_key,'x'), proxies=_config.proxies)
  if (response.status_code == 200):
    rjson = response.json();
    logging.debug( rjson)
  else:
    error = 'Could not get files'
    logging.critical(error)
    raise Exception(error)
    
  for file in rjson:
    logging.debug(file)
    logging.info( file['display_name']+' -- '+file['mtime']+' -- '+file['type'])

  return rjson

def get_file_download_link(filename):
  # Returns an array like:
  # [
  #   {
  #     u'display_name': u'DailySFMC2018, 06, 29.zip',
  #     u'region': u'us-east-1',
  #     u'provided_mtime': u'2018-06-29T07:08:07+00:00',
  #     u'mtime': u'2018-06-29T07:08:08+00:00',
  #     u'crc32': u'3f68b6a6',
  #     u'path': u'etl/Moz_SFDC_Data_Team_Extract/DailySFMC2018, 06, 29.zip',
  #     u'permissions': u'rwd',
  #     u'md5': u'5b57fc2db48b0c860d6803b171819cc4',
  #     u'type': u'file',
  #     u'id': 1182667528,
  #     u'size': 24953177,
  #     u'download_url': "LONG URI HERE",
  #   }
  # ]
  #
  logging.info( "Getting link for file: %s" % filename)
  brickftp_url = _config.api_url + '/files/' + filename
  response = requests.get(brickftp_url, auth=(_config.api_key,'x'), proxies=_config.proxies)
  if (response.status_code == 200):
    rjson = response.json();
    logging.debug( rjson)
  else:
    error = 'Could not get download link'
    logging.critical(error)
    raise Exception(error)
    
  logging.debug( rjson)
  logging.debug( rjson['display_name']+' -- '+rjson['download_uri'])

  return rjson

def delete_file(filename):
  logging.info( "Deleting file: %s" % filename)
  brickftp_url = _config.api_url + '/files/' + filename
  response = requests.delete(brickftp_url, auth=(_config.api_key,'x'), proxies=_config.proxies)
  if (response.status_code == 200):
    logging.debug( "File deleted")
  else:
    error = 'Could not delete file'
    logging.critical(error)
    raise Exception(error)
    

def get_file(filepath,dest_dir='.'):
  link = get_file_download_link(filepath)['download_uri']
  return get_file_from_link(filepath,link,dest_dir)

def get_file_from_link(filepath,dl_link,dest_dir):
  logging.info( "Downloading file %s" % filepath)
  logging.info( "from link: %s" % dl_link)

  if re.search('/',filepath):
    filename = filepath.rsplit('/',1)[1]
  else:
    filename = filepath

  response = requests.get(dl_link, proxies=_config.proxies)
  logging.info( "writing to: %s" % dest_dir + '/' + filename)
  open(os.path.join(dest_dir, filename),'wb').write(response.content)
  return os.path.join(dest_dir, filename)

def move_file(filepath,newfilepath):
  logging.info( "Moving file %s to %s" % (filepath,newfilepath))
 
  brickftp_url = _config.api_url + '/files/' + filepath
  response = requests.post(brickftp_url, auth=(_config.api_key,'x'), data = {'move-destination':newfilepath}, proxies=_config.proxies)
  if (response.status_code == 201):
    logging.debug("File moved")
  else:
    error = 'Could not move file'
    logging.critical(error)
    raise Exception(error)

def upload_file(filename):
  # this is left as an exercise for the reader
  pass
