#!/usr/bin/env python3
#!/usr/local/bin/python2.7

from __future__ import division
import time
import requests
import json,sys,os,errno,re,argparse
from datetime import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import XMatters
import Workday
import Util

parser = argparse.ArgumentParser(description="Sync up XMatters with Workday")
parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
parser.add_argument('-f', '--force', action='store_true', help='force changes even if there are a lot')
#parser.add_argument('--xm-config',   action='store', help='specify an xmatters config file')
#parser.add_argument('--wd-config',   action='store', help='specify a workday config file')
args = parser.parse_args()

debug = args.debug

def print_debug(level, message):
  if debug >= level:
    print("[%s] %s" % (datetime.now(),message))

def user_data_matches(wd_user,xm_user):
  manager_name = ''
  if 'Worker_s_Manager' in wd_user:
    manager_name = wd_user['Worker_s_Manager'][0]['User_Manager_Preferred_First_Name'] + ' ' \
                   + wd_user['Worker_s_Manager'][0]['User_Manager_Preferred_Last_Name']
  site_key = wd_user.get('User_Home_Country','') + ':' + wd_user.get('User_Home_Postal_Code','')
  try:
    if wd_user['User_Preferred_First_Name'] != xm_user['firstName']:
      print_debug(3, "MISMATCH (first name): %s <-> %s" % (wd_user['User_Preferred_First_Name'],xm_user['firstName']))
      return False
    elif wd_user['User_Preferred_Last_Name'] != xm_user['lastName']:
      print_debug(3, "MISMATCH (last name): %s <-> %s" % (wd_user['User_Preferred_Last_Name'],xm_user['lastName']))
      return False
    elif site_key != xm_user['site']['name']:
      print_debug(3, "MISMATCH (site name): %s <-> %s" % (site_key,xm_user['site']['name']))
      return False
    elif wd_user.get('User_Manager_Email_Address','') != xm_user['properties']['Manager Email']:
      print_debug(3, "MISMATCH (manager email): %s <-> %s" % (wd_user['User_Manager_Email_Address'],xm_user['properties']['Manager Email']))
      return False
    elif manager_name != xm_user['properties']['Manager']:
      print_debug(3, "MISMATCH (manager name): %s <-> %s" % (manager_name,xm_user['properties']['Manager']))
      return False
    elif wd_user['User_Cost_Center'] != xm_user['properties']['Cost Center']:
      print_debug(3, "MISMATCH (cost center): %s <-> %s" % (wd_user['User_Cost_Center'],xm_user['properties']['Cost Center']))
      return False
    elif wd_user.get('User_Functional_Group','') != xm_user['properties']['Functional Group']:
      print_debug(3, "MISMATCH (functional group): %s <-> %s" % (wd_user['User_Functional_Group'],xm_user['properties']['Functional Group']))
      return False
    elif wd_user.get('User_Home_City','') != xm_user['properties']['Home City']:
      print_debug(3, "MISMATCH (home city): %s <-> %s" % (wd_user['User_Home_City'],xm_user['properties']['Home City']))
      return False
    elif wd_user.get('User_Home_Country','') != xm_user['properties']['Home Country']:
      print_debug(3, "MISMATCH (home country): %s <-> %s" % (wd_user['User_Home_Country'],xm_user['properties']['Home Country']))
      return False
    elif wd_user.get('User_Home_Postal_Code','') != xm_user['properties']['Home Zipcode']:
      print_debug(3, "MISMATCH (home zipcode): %s <-> %s" % (wd_user['User_Home_Postal_Code'],xm_user['properties']['Home Zipcode']))
      return False
    elif wd_user['User_Work_Location'] != xm_user['properties']['Work Location']:
      print_debug(3, "MISMATCH (Work Location): %s <-> %s" % (wd_user['User_Work_Location'],xm_user['properties']['Work Location']))
      return False
    else:
      return True
  except KeyError:
    print_debug(3, "Some key was not found, assuming a missing field in XMatters")
    return False
  
def iterate_thru_wd_users(wd_users,xm_users,xm_sites):
  wd_users_seen = {}
  for user in wd_users:
    if 'User_Email_Address' not in user:
      print("Workday User ID %s (%s) has no email address! Skipping." % \
        (user['User_Employee_ID'], user['User_Preferred_First_Name'] + ' ' + user['User_Preferred_Last_Name']))
      continue
    elif not re.search('(?:mozilla.com|mozillafoundation.org|getpocket.com)$',user['User_Email_Address']):
      print_debug(3, "User {} has non-matching email. Skipping.".format(user['User_Email_Address']))
      continue
    wd_users_seen[ user['User_Email_Address'] ] = 1
    if user['User_Email_Address'] in xm_users:
      print_debug(5, "User %s found in XM" % user['User_Email_Address'])
      if not user_data_matches(user,xm_users[ user['User_Email_Address'] ]):
        print_debug(5, "USER DATA NO MATCHES!")
        XMatters.update_user(user,xm_users[ user['User_Email_Address'] ], xm_sites)
      else:
        print_debug(5, "%s good" % user['User_Email_Address'])
    else:
      # add user to XM
      XMatters.add_user(user, xm_sites)
      #time.sleep(5)

  return wd_users_seen

def get_wd_sites_from_users(users):
  unique_sites = {}
  for user in users:
    city    = user.get('User_Home_City','')
    country = user.get('User_Home_Country','')
    postal  = user.get('User_Home_Postal_Code','')
    unq_key = country + ':' + postal
    if not country:
      print()
      print()
      print()
      print("NO COUNTRY!!")
      print(user)
      country = 'United States of America'
    if not postal:
      print()
      print()
      print()
      print("NO POSTAL!!")
      print(user)
      postal = '97209'

    if unq_key not in unique_sites:
#      query_dict = {'country': country, 'postal_code': postal}
#      if city:
#        query_dict['city'] = city
#      (coords, tz) = Util.postal_to_coords_and_timezone(query_dict)
#      if tz == None:
#        tz = 'America/Los_Angeles' # arbitrary
#      if coords == (None, None):
#        coords = (0, 0)
      unique_sites[unq_key] = {
        'name'       : unq_key,
#        'timezone'   : str(tz),
        'country'    : country,
        'city'       : city,
        'postal_code': postal,
#        'latitude'   : coords[0],
#        'longitude'  : coords[1],
      }
      print(unq_key)
      print(unique_sites[unq_key])

  return unique_sites

if __name__ == "__main__":
 
  print_debug(1, "Starting...")

  XMatters.debug(debug)
  Workday.debug(debug)
  Util.debug(debug)

  #XMatters.is_production(False)

  # get all sites in xmatters
  xm_sites = XMatters.get_all_sites()

  # get all users from workday
  wd_users = Workday.get_users()

  # get the new style (zipcodes) sites from the user list
  wd_sites = get_wd_sites_from_users(wd_users)

#  # get list of sites from workday users
#  wd_sites = Workday.get_sites()

  sites_percentage = len(xm_sites) / len(wd_sites)
  if sites_percentage > 1.1 or sites_percentage < 0.9:
    print_debug(1, "The number of sites in Workday vs XMatters is different by more than 10%% (%.02f%%)." % (abs(100-sites_percentage*100)))
    print_debug(1, "Stopping unless --force")
    if not args.force:
      exit()

  # add any sites in workday that aren't in xmatters to xmatters
  xm_sites_in_wd = XMatters.add_new_sites(wd_sites,xm_sites)

  # delete any sites NOT in workday that ARE in xmatters
  #XMatters.delete_sites(xm_sites,xm_sites_in_wd)
  
  # get all users from xmatters
  xm_users = XMatters.get_all_people()

  users_percentage = len(xm_users) / len(wd_users)
  if users_percentage > 1.1 or users_percentage < 0.9:
    print_debug(1, "The number of users in Workday vs XMatters is different by more than 10%% (%.02f%%)." % (abs(100-users_percentage * 100)))
    print_debug(1, "Stopping unless --force")
    if not args.force:
      exit()

  # iterate thru users in workday:
  #   if not in xmatters, add to xmatters
  #   if data doesn't match xmatters, update xmatters
  #   mark-as-seen in xmatters
  users_seen_in_workday = iterate_thru_wd_users(wd_users,xm_users,xm_sites)
  
  # iterate through xmatters users who aren't marked-as-seen
  #   remove from xmatters
  XMatters.delete_users(xm_users,users_seen_in_workday)

  print_debug(1, "Finished.")
