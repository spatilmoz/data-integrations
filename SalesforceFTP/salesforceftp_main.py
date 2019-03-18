import time
from ftplib import FTP
import json,sys,os,errno,re
from secrets_salesforceftp import config as salesforceftp_config
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LocalConfig(object):
  def __init__(self):
    self.ftp_host = 'ftp.s4.exacttarget.com'
    self.debug    = 3

  def __getattr__(self, attr):
    return salesforceftp_config[attr]

_config = LocalConfig()

ftp_obj = FTP(host=_config.hostname, user=_config.username, passwd=_config.password)

def list_files(path='/'):
  logger.info( "Listing files for path: %s" % path)
  return ftp_obj.mlsd(path=path)

def delete_file(filename):
  # UNIMPLEMENTED
  return
  logger.info( "Deleting file: %s" % filename)
  brickftp_url = _config.api_url + '/files/' + filename
  response = requests.delete(brickftp_url, auth=(_config.api_key,'x'), proxies=_config.proxies)
  if (response.status_code == 200):
    logger.debug( "File deleted")
  else:
    error = 'Could not delete file'
    logger.critical(error)
    raise Exception(error)
    

def get_file(path, filename, dest_dir='.'):
  logger.info( "Downloading file %s" % filename)

  ftp_obj.cwd(path)
  ftp_obj.retrbinary('RETR %s' % filename, open(os.path.join(dest_dir, filename), 'wb').write)

def move_file(filepath,newfilepath):
  # UNIMPLEMENTED
  return
  logger.info( "Moving file %s to %s" % (filepath,newfilepath))
 
  brickftp_url = _config.api_url + '/files/' + filepath
  response = requests.post(brickftp_url, auth=(_config.api_key,'x'), data = {'move-destination':newfilepath}, proxies=_config.proxies)
  if (response.status_code == 201):
    logger.debug("File moved")
  else:
    error = 'Could not move file'
    logger.critical(error)
    raise Exception(error)

def upload_file(filename):
  # this is left as an exercise for the reader
  pass
