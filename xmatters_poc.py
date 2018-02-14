#!/usr/local/bin/python2.7

import requests
import json,sys,os,errno,re,argparse
from datetime import datetime
import XMatters
from secret import config

parser = argparse.ArgumentParser(description="Sync up XMatters with Workday")
parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
args = parser.parse_args()

debug = args.debug

proxies = {"https" : "http://proxy.dmz.scl3.mozilla.com:3128"}

def print_debug(level, message):
  if debug >= level:
    print "[%s] %s" % (datetime.now(),message)

def get_workday_users():
  print_debug(3,"\n")
  print_debug(1,"Gathering all Workday people")
  try:
    #r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/sstorey/IT_Data_Warehouse_Worker_Sync_Full_File?format=json',auth=(config['wd_username'],config['wd_password']),proxies=proxies)
    r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/sstorey/IT_Data_Warehouse_Worker_Sync_Full_File?format=json',auth=(config['wd_username'],config['wd_password']))
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

def user_data_matches(wd_user,xm_user):
  try:
    if wd_user['First_Name'] != xm_user['firstName']:
      print_debug(3, "MISMATCH: %s <-> %s" % (wd_user['First_Name'],xm_user['firstName']))
      return False
    elif wd_user['Last_Name'] != xm_user['lastName']:
      print_debug(3, "MISMATCH: %s <-> %s" % (wd_user['Last_Name'],xm_user['lastName']))
      return False
    elif wd_user['Location'] != xm_user['site']['name']:
      print_debug(3, "MISMATCH: %s <-> %s" % (wd_user['Location'],xm_user['site']['name']))
      return False
    elif wd_user['Manager_Name'] != xm_user['properties']['Manager']:
      print_debug(3, "MISMATCH: %s <-> %s" % (wd_user['Manager_Name'],xm_user['properties']['Manager']))
      return False
    elif wd_user['Cost_Center'] != xm_user['properties']['Cost Center']:
      print_debug(3, "MISMATCH: %s <-> %s" % (wd_user['Cost_Center'],xm_user['properties']['Cost Center']))
      return False
    elif wd_user['Functional_Group'] != xm_user['properties']['Functional Group']:
      print_debug(3, "MISMATCH: %s <-> %s" % (wd_user['Functional_Group'],xm_user['properties']['Functional Group']))
      return False
    else:
      return True
  except KeyError:
    print_debug(3, "Some key was not found, assuming a missing field in XMatters")
    return False
  
def iterate_thru_wd_users(wd_users,xm_users,xm_sites):
  wd_users_seen = {}
  for user in wd_users:
    if not user.has_key('Email_Address'):
      print "WORKDAY USER ID %s (%s) HAS NO EMAIL ADDRESS! SKIPPING. THIS SHOULD BE FIXED IN WORKDAY" % \
        (user['Employee_ID'], user['First_Name'] + ' ' + user['Last_Name'])
      continue
    wd_users_seen[ user['Email_Address'] ] = 1
    if user['Email_Address'] in xm_users:
      print_debug(5, "User %s found in XM" % user['Email_Address'])
      if not user_data_matches(user,xm_users[ user['Email_Address'] ]):
        print_debug(5, "USER DATA NO MATCHES!")
        XMatters.update_user(user,xm_users[ user['Email_Address'] ], xm_sites)
      else:
        print_debug(5, "%s good" % user['Email_Address'])
    else:
      # add user to XM
      XMatters.add_user(user, xm_sites)

  return wd_users_seen

if __name__ == "__main__":
 
  print_debug(1, "Starting...")

  XMatters.debug = debug

  # get all sites in xmatters
  xm_sites = XMatters.get_all_sites()

  # get all users from workday
  wd_users = get_workday_users()

  # get list of sites from workday users
  wd_sites = extract_sites_from_wd(wd_users)

  # add any sites in workday that aren't in xmatters to xmatters
  xm_sites_in_wd = XMatters.add_new_sites(wd_sites,xm_sites)

  # delete any sites NOT in workday that ARE in xmatters
  XMatters.delete_sites(xm_sites,xm_sites_in_wd)
  
  # get all users from xmatters
  xm_users = XMatters.get_all_people()
  
  # iterate thru users in workday:
  #   if not in xmatters, add to xmatters
  #   if data doesn't match xmatters, update xmatters
  #   mark-as-seen in xmatters
  users_seen_in_workday = iterate_thru_wd_users(wd_users,xm_users,xm_sites)
  
  # iterate through xmatters users who aren't marked-as-seen
  #   remove from xmatters
  XMatters.delete_users(xm_users,users_seen_in_workday)

  print_debug(1, "Finished.")
