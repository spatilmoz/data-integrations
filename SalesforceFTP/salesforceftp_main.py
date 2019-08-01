import logging
import os
from ftplib import FTP
from subprocess import call

from SalesforceFTP.secrets_salesforceftp import config as salesforceftp_config

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

def get_file_stupid_way(path, filename, dest_dir='.'):
  logger.info( "Downloading file %s the stupid way" % filename)

  if 'https' in _config.proxies:
    command_string = "set ftp:proxy %s; open %s; USER %s %s; GET %s; quit" % ( _config.proxies['https'], _config.hostname, _config.username, _config.password, os.path.join(path, filename))
  else:
    command_string = "open %s; USER %s %s; GET %s; quit" % ( _config.hostname, _config.username, _config.password, os.path.join(path, filename))
  call(['lftp', '-e', command_string], cwd=dest_dir)


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
