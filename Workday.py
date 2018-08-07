import requests
import json,sys,os,errno,re,argparse
from datetime import datetime
from secrets_workday import config as wd_config

class LocalConfig(object):
  def __init__(self):
    self.proxies             = {'https' : 'http://proxy.dmz.scl3.mozilla.com:3128'}
    self.debug               = 3
    self.workday_url_prefix  = 'https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/ISU_RAAS/'
    self.workday_sites_url   = self.workday_url_prefix + 'Mozilla_BusContSites?format=json'
    self.workday_people_url  = self.workday_url_prefix + 'Mozilla_BusContUsers?format=json'
    self.workday_seating_url = self.workday_url_prefix + 'WPR_Worker_Space_Number?format=json'
    # TODO: This should move to the XMatters module:
    self.workday_to_xmatters_tz = {
      'GMT United Kingdom Time (London)'                         : 'GMT',
      'GMT Western European Time (Casablanca)'                   : 'GMT',
      'GMT+01:00 Central European Time (Amsterdam)'              : 'Europe/Amsterdam',
      'GMT+01:00 Central European Time (Berlin)'                 : 'Europe/Berlin',
      'GMT+01:00 Central European Time (Oslo)'                   : 'Europe/Oslo',
      'GMT+01:00 Central European Time (Paris)'                  : 'Europe/Paris',
      'GMT+01:00 Central European Time (Prague)'                 : 'Europe/Prague',
      'GMT+01:00 Central European Time (Stockholm)'              : 'Europe/Stockholm',
      'GMT+02:00 Eastern European Time (Athens)'                 : 'Europe/Athens',
      'GMT+02:00 Eastern European Time (Bucharest)'              : 'Europe/Bucharest',
      'GMT+02:00 Eastern European Time (Helsinki)'               : 'Europe/Helsinki',
      'GMT+02:00 Israel Time (Jerusalem)'                        : 'Europe/Kaliningrad',
      'GMT+02:00 South Africa Standard Time (Johannesburg)'      : 'Africa/Johannesburg',
      'GMT+03:00 East Africa Time (Nairobi)'                     : 'Africa/Nairobi',
      'GMT+03:00 Moscow Standard Time (Moscow)'                  : 'Europe/Moscow',
      'GMT+05:00 Pakistan Standard Time (Karachi)'               : 'Asia/Karachi',
      'GMT+05:00 Yekaterinburg Standard Time (Yekaterinburg)'    : 'Asia/Yekaterinburg',
      'GMT+05:30 India Standard Time (Kolkata)'                  : 'Asia/Kolkata',
      'GMT+06:00 East Kazakhstan Time (Almaty)'                  : 'Asia/Almaty',
      'GMT+07:00 Indochina Time (Ho Chi Minh City)'              : 'Asia/Ho_Chi_Minh',
      'GMT+07:00 Western Indonesia Time (Jakarta)'               : 'Asia/Jakarta',
      'GMT+08:00 Australian Western Standard Time (Perth)'       : 'Australia/Perth',
      'GMT+08:00 China Standard Time (Shanghai)'                 : 'Asia/Shanghai',
      'GMT+08:00 Singapore Standard Time (Singapore)'            : 'Asia/Singapore',
      'GMT+08:00 Taipei Standard Time (Taipei)'                  : 'Asia/Taipei',
      'GMT+08:00 Hong Kong Standard Time (Hong Kong)'            : 'Asia/Hong_Kong',
      'GMT+09:00 Japan Standard Time (Tokyo)'                    : 'Asia/Tokyo',
      'GMT+09:30 Australian Central Standard Time (Darwin)'      : 'Australia/Darwin',
      'GMT+10:00 Australian Eastern Standard Time (Brisbane)'    : 'Australia/Brisbane',
      'GMT+12:00 New Zealand Time (Auckland)'                    : 'Australia/Brisbane',
      'GMT-03:00 Argentina Standard Time (Buenos Aires)'         : 'America/Buenos_Aires',
      'GMT-03:00 Brasilia Standard Time (Recife)'                : 'America/Recife',
      'GMT-03:30 Newfoundland Time (St. John\'s)'                : 'America/St_Johns',
      'GMT-04:00 Atlantic Time (Halifax)'                        : 'America/Halifax',
      'GMT-05:00 Colombia Standard Time (Bogota)'                : 'America/Bogota',
      'GMT-05:00 Eastern Time (Indianapolis)'                    : 'America/Indiana/Indianapolis',
      'GMT-05:00 Eastern Time'                                   : 'America/New_York',
      'GMT-05:00 Eastern Time (New York)'                        : 'America/New_York',
      'GMT-06:00 Central Standard Time (Regina)'                 : 'America/Regina',
      'GMT-06:00 Central Time'                                   : 'America/Chicago',
      'GMT-06:00 Central Time (Chicago)'                         : 'America/Chicago',
      'GMT-06:00 Central Time (Mexico City)'                     : 'America/Mexico_City',
      'GMT-07:00 Mountain Standard Time (Phoenix)'               : 'America/Phoenix',
      'GMT-07:00 Mountain Time'                                  : 'America/Phoenix',
      'GMT-07:00 Mountain Time (Denver)'                         : 'America/Denver',
      'GMT-08:00 Pacific Time'                                   : 'America/Los_Angeles',
      'GMT-08:00 Pacific Time (Los Angeles)'                     : 'America/Los_Angeles',
      'GMT-08:00 Pacific Time (Tijuana)'                         : 'America/Tijuana',
      'GMT-10:00 Hawaii-Aleutian Standard Time (Honolulu)'       : 'America/Anchorage',
    }

  def __getattr__(self, attr):
    return wd_config[attr]

_config = LocalConfig()

def debug(debug=None):
  if debug == None:
    return _config.debug
  else:
    _config.debug = debug

def print_debug(level, message):
  if _config.debug >= level:
    print("[%s] %s" % (datetime.now(),message))

def get_users():
  print_debug(3,"\n")
  print_debug(1,"Gathering all Workday people")
  try:
    #r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/sstorey/IT_Data_Warehouse_Worker_Sync_Full_File?format=json',auth=(_config.wd_username,_config.wd_password),proxies=proxies)
    r = requests.get(_config.workday_people_url,auth=(_config.wd_username,_config.wd_password))
    results = json.loads(r.text)
    return results['Report_Entry']
  except:
    print(sys.exc_info()[0])
    raise

def get_seating():
  print_debug(3,"\n")
  print_debug(1,"Gathering all Workday seating")
  try:
    r = requests.get(_config.workday_seating_url,auth=(_config.wd_seating_username,_config.wd_seating_password))
    results = json.loads(r.text)
    wd_seating_chart = {}
    for seat in results['Report_Entry']:
        if seat['Employment_Status'] == 'Terminated':
          continue
        wd_seating_chart[ seat['Employee_ID'] ] = seat.get('WPR_Desk_Number','')

    return wd_seating_chart
    
  except:
    print(sys.exc_info()[0])
    raise

def get_sites():
  print_debug(3,"\n")
  print_debug(1,"Gathering all Workday sites")
  try:
    r = requests.get(_config.workday_sites_url,auth=(_config.wd_username,_config.wd_password))
    results = json.loads(r.text)
    #return results['Report_Entry']
    wd_locations = {}
    for site in results['Report_Entry']:
      name = site['Work_Location_Name']
      if name in wd_locations:
        continue
      else:
        if re.search('^GMT-03:30 Newfoundland Time',site.get('Work_Location_Timezone','')):
          # fixup a stupid non-ascii character
          site['Work_Location_Timezone'] = 'GMT-03:30 Newfoundland Time (St. John\'s)'

        wd_locations[ name ] = {
          'name':        name,
          'timezone':    _config.workday_to_xmatters_tz[ site.get('Work_Location_Timezone','') ],
          'address':     site.get('Work_Location_Address',''),
          'country':     site.get('Work_Location_Country',''),
          'city':        site.get('Work_Location_City',''),
          'state':       site.get('Work_Location_State',''),
          'postal_code': site.get('Work_Location_Postal_Code',''),
        }
    return wd_locations
    
  except:
    print(sys.exc_info()[0])
    raise

#def extract_sites_from_wd(wd_users):
#  print_debug(3,"\n")
#  print_debug(1,"Extracting sites from Workday data")
#  wd_locations = {}
#  for user in wd_users:
#    if user['Location'] in wd_locations:
#      wd_locations[user['Location']] += 1
#    else:
#      wd_locations[user['Location']] = 1
#  print_debug(3, wd_locations)
#  return wd_locations

