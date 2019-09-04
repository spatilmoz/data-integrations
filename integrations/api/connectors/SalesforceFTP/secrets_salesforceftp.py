
import os
config = {
  'proxies'  : {},
  'hostname' : os.environ.get('SALESFORCE_FTP_HOSTNAME','ftp.s4.exacttarget.com'),
  'username' : os.environ.get('SALESFORCE_FTP_USERNAME',''),
  'password' : os.environ.get('SALESFORCE_FTP_PASSWORD',''),
}
