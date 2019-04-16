import requests
import json,sys,os,errno,re,argparse
import datetime
import logging
from .secrets_workday import config as wd_config

logger = logging.getLogger(__name__)

class LocalConfig(object):
  def __init__(self):
    self.debug               = 3
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

def get_users():
  """Gets all users from Workday

  Returns a list of dicts, each dict is an employee:
  [
    {
      u'User_Home_Country': u'United States of America',
      u'User_Home_City': u'Portland',
      u'User_Functional_Group': u'IT',
      u'User_Preferred_First_Name': u'Chris',
      u'Worker_s_Manager': [
        {
          u'User_Manager_Preferred_Last_Name': u'Bixby',
          u'User_Manager_Preferred_First_Name': u'Bill'
        }],
      u'User_Cost_Center': u'1440 - Enterprise Applications and Services (EApps)',
      u'User_Email_Address': u'test@mozilla.com',
      u'User_Work_Location': u'Portland Office',
      u'User_Preferred_Last_Name': u'Test',
      u'User_Employee_ID': u'12345678',
      u'User_Home_Postal_Code': u'90210',
      u'User_Manager_Email_Address': u'thehulk@mozilla.com'},
    {...},
    ...
  ]
  """

  logger.info("Gathering all Workday people")
  try:
    r = requests.get(_config.xmatters_integration['people_url'],auth=(_config.xmatters_integration['username'],_config.xmatters_integration['password']),proxies=_config.proxies)
    results = json.loads(r.text)
    return results['Report_Entry']
  except:
    logger.critical(sys.exc_info()[0])
    raise

def get_seating():
  """Gets all employee IDs and seat assignments

  Parameters:
    None
  Returns:
    dict: employee ID -> WPR_Desk_Number
  """

  logger.info("Gathering all Workday seating")
  try:
    r = requests.get(_config.seating['url'],auth=(_config.seating['username'],_config.seating['password']),proxies=_config.proxies)
    results = json.loads(r.text)
    wd_seating_chart = {}
    for seat in results['Report_Entry']:
        if seat['Employment_Status'] == 'Terminated':
          continue
        wd_seating_chart[ seat['Employee_ID'] ] = seat.get('WPR_Desk_Number','')

    return wd_seating_chart
    
  except:
    logger.critical(sys.exc_info()[0])
    raise

def get_sites():
  """Gets all sites from workday

  Parameters:
    None
 
  Returns:
    dict: a dict with location names as keys and the values are a dict like:
        {
          'name':        'Location Name',
          'timezone':    'Timezone converted to xMatters style',
          'address':     'Location Address',
          'country':     'Location Country',
          'city':        'Location City',
          'state':       'Location State',
          'postal_code': 'Location Postal Code',
        }

    One could successfully argue that the timezone format conversion should not happen here.


  """

  logger.info("Gathering all Workday sites")
  try:
    r = requests.get(_config.xmatters_integration['sites_url'],auth=(_config.xmatters_integration['username'],_config.xmatters_integration['password']),proxies=_config.proxies)
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
    logger.critical(sys.exc_info()[0])
    raise

def date_x_days_from(date, delta_days):
  # TODO: move this to a util module
  if type(date) is str:
    date_l = [ int(i) for i in date.split('-') ]
    date   = datetime.date(date_l[0], date_l[1], date_l[2])
  else:
    # assume it's already a datetime obj?
    pass

  # now that "date" is a datetime object:
  return str(date + datetime.timedelta(days=int(delta_days)))

def get_dashboard_data(type, end_date, start_date=None):
  logger.info("Gathering Workday People %s data" % type)

  if not re.match('^\d{4}-\d{2}-\d{2}$', end_date):
    raise Exception("End Date does not match expected format")

  if type == 'headcount':
    url = _config.hr_dashboard['urls'][type] + '&Effective_as_of_Date_and_Time=' + end_date + \
            'T23%3A59%3A59.000-07%3A00'      + '&Entry_Date_and_Time='           + end_date + \
            'T23%3A59%3A59.000-07%3A00'
  else:
    if not start_date:
      # if no start date is provided, grab the last 7 days
      start_date = date_x_days_from(end_date, '-6')

    url = _config.hr_dashboard['urls'][type]    + '&Effective_End_Date=' + end_date + \
          '&Effective_Start_Date=' + start_date + '&Effective_as_of_Date=' + end_date + \
          '-07%3A00' + '&Entry_Date=' + end_date + '-07%3A00'

  logger.debug("Will grab url: %s" % url)

  return get_generic_workday_report(url,_config.hr_dashboard['username'],_config.hr_dashboard['password'])

def get_ta_dashboard_data(type, end_date, start_date=None):
  logger.info("Gathering Workday TA %s data" % type)

  if not re.match('^\d{4}-\d{2}-\d{2}$', end_date):
    raise Exception("End Date does not match expected format")

  if type == 'hires':
    # FIXME: Hardcoded dates
    url = _config.ta_dashboard['urls'][type] + '&Effective_as_of_Date=2021-12-31-07%3A00' + \
                                               '&Entry_Date=' + end_date + '-07%3A00'     + \
                                               '&Effective_Start_Date=2017-01-01-07%3A00' + \
                                               '&Effective_End_Date=2021-12-31-07%3A00'

  logger.debug("Will grab url: %s" % url)

  return get_generic_workday_report(url,_config.ta_dashboard['username'],_config.ta_dashboard['password'])

def get_generic_workday_report(url,uname,pword):
  try:
    r = requests.get(url,auth=(uname,pword), proxies=_config.proxies)
    r.encoding = "utf-8" # otherwise requests thinks it's ISO-8859-1
    return(r.text)
  except:
    logger.critical(sys.exc_info()[0])
    raise

