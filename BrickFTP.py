import time
import requests
import json,sys,os,errno,re
from secrets_brickftp import config as brickftp_config
from datetime import datetime

class LocalConfig(object):
  def __init__(self):
    self.api_url  = 'https://mozilla.brickftp.com/api/rest/v1/'
    self.proxies  = {'https' : 'http://proxy.dmz.scl3.mozilla.com:3128'}
    self.debug    = 3

  def __getattr__(self, attr):
    return brickftp_config[attr]

_config = LocalConfig()

def print_debug(level, message):
  if _config.debug >= level:
    print "[%s] %s" % (datetime.now(),message)

def debug(debug=None):
  if debug == None:
    return _config.debug
  else:
    _config.debug = debug

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
  print_debug(1, "Listing files for path: %s" % path)
  brickftp_url = _config.api_url + '/folders/' + path
  response = requests.get(brickftp_url, auth=(_config.api_key,'x'))
  if (response.status_code == 200):
    rjson = response.json();
    print_debug(5, rjson)
  else:
    error = 'Could not get files'
    print error
    raise Exception(error)
    
  for file in rjson:
    print_debug(5, file)
    print_debug(3, file['display_name']+' -- '+file['mtime']+' -- '+file['type'])

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
  print_debug(1, "Getting link for file: %s" % filename)
  brickftp_url = _config.api_url + '/files/' + filename
  response = requests.get(brickftp_url, auth=(_config.api_key,'x'))
  if (response.status_code == 200):
    rjson = response.json();
    print_debug(5, rjson)
  else:
    error = 'Could not get download link'
    print error
    raise Exception(error)
    
  print_debug(5, rjson)
  print_debug(4, rjson['display_name']+' -- '+rjson['download_uri'])

  return rjson

def delete_file(filename):
  print_debug(1, "Deleting file: %s" % filename)
  brickftp_url = _config.api_url + '/files/' + filename
  response = requests.delete(brickftp_url, auth=(_config.api_key,'x'))
  if (response.status_code == 200):
    print_debug(5, "File deleted")
  else:
    error = 'Could not delete file'
    print error
    raise Exception(error)
    

def get_file(filepath,dest_dir='.'):
  link = get_file_download_link(filepath)['download_uri']
  return get_file_from_link(filepath,link,dest_dir)

def get_file_from_link(filepath,dl_link,dest_dir):
  print_debug(3, "\n")
  print_debug(1, "Downloading file %s" % filepath)
  print_debug(4, "from link: %s" % dl_link)

  if re.search('/',filepath):
    filename = filepath.rsplit('/',1)[1]
  else:
    filename = filepath

  response = requests.get(dl_link)
  print_debug(3, "writing to: %s" % dest_dir + '/' + filename)
  open(os.path.join(dest_dir, filename),'wb').write(response.content)
  return os.path.join(dest_dir, filename)

def move_file(filepath,newfilepath):
  print_debug(3, "\n")
  print_debug(1, "Moving file %s to %s" % (filepath,newfilepath))
 
  brickftp_url = _config.api_url + '/files/' + filepath
  response = requests.post(brickftp_url, auth=(_config.api_key,'x'), data = {'move-destination':newfilepath})
  if (response.status_code == 201):
    print_debug(5, "File moved")
  else:
    error = 'Could not move file'
    print error
    raise Exception(error)

def upload_file(filename):
  # this is left as an exercise for the reader
  pass
