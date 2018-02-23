import requests
import json,sys,os,errno,re,argparse
from datetime import datetime
from secrets_workday import config

class LocalConfig(object):
  def __init__(self):
    self.proxies          = {"https" : "http://proxy.dmz.scl3.mozilla.com:3128"}
    self.debug            = 3

  def __getattr__(self, attr):
    return config[attr]

_config = LocalConfig()

def debug(debug=None):
  if debug == None:
    return _config.debug
  else:
    _config.debug = debug

def print_debug(level, message):
  if _config.debug >= level:
    print "[%s] %s" % (datetime.now(),message)

def get_workday_users():
  print_debug(3,"\n")
  print_debug(1,"Gathering all Workday people")
  try:
    #r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/sstorey/IT_Data_Warehouse_Worker_Sync_Full_File?format=json',auth=(_config.wd_username,_config.wd_password),proxies=proxies)
    r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/sstorey/IT_Data_Warehouse_Worker_Sync_Full_File?format=json',auth=(_config.wd_username,_config.wd_password))
    results = json.loads(r.text)
    return results['Report_Entry']
  except:
    print(sys.exc_info()[0])
    raise

def extract_sites_from_wd(wd_users):
  print_debug(3,"\n")
  print_debug(1,"Extracting sites from Workday data")
  wd_locations = {}
  for user in wd_users:
    if user['Location'] in wd_locations:
      wd_locations[user['Location']] += 1
    else:
      wd_locations[user['Location']] = 1
  print_debug(3, wd_locations)
  return wd_locations

