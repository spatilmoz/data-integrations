import time
import requests
import json,sys,os,errno,re
from datetime import datetime
from .secrets_xmatters import config as xm_config

#xm_config = {}
#
#def load_config(config_path):
#  global xm_config
#  if config_path and os.path.isfile(config_path):
#    exec(open(config_path).read())
#    xm_config = config
#  else:
#    try:
#      from .secrets_xmatters import config as xm_config
#    except:
#      raise Exception("No XMatters config file found!")
      

class LocalConfig(object):
  def __init__(self):
    host_dev                   = 'mozilla-np'
    host_prod                  = 'mozilla'
    new_api_suffix             = '/api/xm/1'
    old_api_suffix             = '/reapi/2015-04-01/'
    self.debug                 = 3
    self.base_URL_dev          = 'https://' + host_dev  + '.xmatters.com' + new_api_suffix
    self.base_URL_prod         = 'https://' + host_prod + '.xmatters.com' + new_api_suffix
    self.base_URL_old_api_dev  = 'https://' + host_dev  + '.xmatters.com' + old_api_suffix
    self.base_URL_old_api_prod = 'https://' + host_prod + '.xmatters.com' + old_api_suffix
    self.base_URL_no_path_dev  = 'https://' + host_dev  + '.xmatters.com'
    self.base_URL_no_path_prod = 'https://' + host_prod + '.xmatters.com'
    self.production            = False
    self.supervisor_id_dev     = '72a77545-4c4b-465d-b22a-41a14e0a1b78'
    self.supervisor_id_prod    = '6cc72a91-2b6d-4bf0-8551-019bd2e9e87c'
    self.access_token          = False

  def __getattr__(self, attr):
    return xm_config[attr]

_config = LocalConfig()

def print_debug(level, message):
  if _config.debug >= level:
    print("[%s] %s" % (datetime.now(),message))

def debug(debug=None):
  if debug == None:
    return _config.debug
  else:
    _config.debug = debug

def is_production(is_prod=None):
  if is_prod == None:
    return _config.production
  elif is_prod:
    _config.base_URL         = _config.base_URL_prod
    _config.base_URL_old_api = _config.base_URL_old_api_prod
    _config.base_URL_no_path = _config.base_URL_no_path_prod
    _config.supervisor_id    = _config.supervisor_id_prod
    _config.production       = True
  else:
    _config.base_URL         = _config.base_URL_dev
    _config.base_URL_old_api = _config.base_URL_old_api_dev
    _config.base_URL_no_path = _config.base_URL_no_path_dev
    _config.supervisor_id    = _config.supervisor_id_dev
    _config.production       = False

def get_access_token():
  if not _config.access_token:
    _config.access_token = _get_access_token()
  return _config.access_token

def _get_access_token():
  endpoint_URL = '/oauth2/token' 
  grant_type='password'
  url = _config.base_URL + endpoint_URL +'?grant_type='+grant_type+'&client_id='+_config.xm_client_id+'&username='+_config.xm_username+'&password='+_config.xm_password

  headers = {'Content-Type': 'application/json'}

  response = requests.post(url, headers=headers, proxies=_config.proxies)

  if (response.status_code == 200):
     rjson = response.json();
     print_debug(5, 'Access token: ' + rjson.get('access_token') + ', \nRefresh token: ' + rjson.get('refresh_token'))
     access_token = rjson.get('access_token')
  else:
     error = 'Could not get an access token'
     print(error)
     raise Exception(error)

  return access_token

# get all xmatters sites
# OLD API
# https://help.xmatters.com/OnDemand/xmodwelcome/communicationplanbuilder/appendixrestapi.htm?cshid=apiGETsites#GETsites
#
def get_all_sites():
  """Gets all sites from xMatters

  Parameters:
    None

  Returns:
    dict: site name -> xmatters site id
      for all sites with status "ACTIVE"

  Example:
    {
      [...]
      'US Remote (NV)' : '656173de-809d-46c3-82f3-dd718efa6af4',
      'Israel Remote'  : '7ed98c24-c73f-4fa5-b987-a005e80e2d63',
      'US Remote (NM)' : '5224215b-337f-4c6b-bc6a-6211246e2086',
      'US Remote (LA)' : '96c2de74-247d-4bb8-b0ec-592b86768f85',
      [...]
    }
  """

  print_debug(3, "\n")
  print_debug(1, "Gathering all XMatters sites")
  all_sites_url = _config.base_URL_old_api + 'sites'
  xm_sites = {}
  while True:
    response = requests.get(all_sites_url, auth=(_config.xm_username,_config.xm_password), proxies=_config.proxies)
    if (response.status_code == 200):
      rjson = response.json();
      print_debug(5, rjson)
    else:
      error = 'Could not get sites'
      print(error)
      raise Exception(error)
    
    for site in rjson['sites']:
      print_debug(3, site['name']+' -- '+site['identifier'])
      print_debug(5, site)
      if site['status'] == 'ACTIVE':
        xm_sites[ site['name'] ] = site['identifier']
      else:
        print_debug(2, "Skipping XMatters site %s because status is %s" % (site['name'],site['status']))

    if rjson['nextRecordsURL'] == '':
      print_debug(5, "No nextRecordsURL found. done with fetching")
      break
    else:
      print_debug(5,"NEXT RECORDS URL FOUND: %s" % rjson['nextRecordsURL'])
      all_sites_url = _config.base_URL_no_path + rjson['nextRecordsURL']

  return xm_sites

# get all people from xmatters
# NEW API
# https://help.xmatters.com/xmAPI/?python#get-people
#
def get_all_people():
  """Gets all users/people from xMatters

  Parameters:
    None

  Returns:
    dict: name -> { attributes }

  Example:
    {
      [...]
      'test@mozilla.com' : {
        u'recipientType': u'PERSON',
        u'status': u'ACTIVE',
        u'firstName': u'Chris',
        u'lastName': u'Test',
        u'links': {u'self': u'/api/xm/1/people/fc97c634-6e9b-4788-bdca-xxxxxxxxxxxx'},
        u'externallyOwned': False,
        u'site': {
          u'id': u'2e6f8d1c-ced7-460e-bf5a-902109021090',
          u'links': { u'self': u'/api/xm/1/sites/2e6f8d1c-ced7-460e-bf5a-902109021090' },
          u'name': u'Beverly Hills Office'
        },
        u'properties': {
          u'Functional Group': u'IT',
          u'Executive': False,
          u'Manager Email': u'bbixby@mozilla.com',
          u'Home Country': u'United States of America',
          u'Cost Center': u'1440 - Enterprise Applications and Services (EApps)',
          u'Manager': u'Bill Bixby',
          u'Home Zipcode': u'90210',
          u'MERT/EVAC/Warden': False,
          u'Home City': u'Beverly Hills'
        },
        u'language': u'en',
        u'webLogin': u'test@mozilla.com',
        u'timezone': u'US/Pacific',
        u'targetName': u'test@mozilla.com',
        u'id': u'fc97c634-6e9b-4788-bdca-xxxxxxxxxxxx'
      },
      [...]
    }
  """

  print_debug(3, "\n")
  print_debug(1, "Gathering all XMatters people")
  url = _config.base_URL + '/people'

  headers = {'Authorization': 'Bearer ' + get_access_token()}

  xm_people = {}
  while True:
    response = requests.get(url, headers=headers, proxies=_config.proxies)

    if (response.status_code == 200):
      rjson = response.json()
      print_debug(2, 'Retrieved ' + str(rjson['count']) + ' of ' + str(rjson['total']) + " people.")
    else:
      print(response)
      raise Exception(response.content)
  
    for person in rjson['data']:
      print_debug(4, "%s %s (%s)" % (person['firstName'],person['lastName'],person['targetName']))
      if person['lastName'] == 'Valaas':
        print_debug(3, person)
      xm_people[ person['targetName'] ] = person
 
# Only to backfill data
#      devs = get_devices_by_person(person['id'])
#      if not devs:
#        add_work_email_device(person)

    if 'next' in rjson['links']:
      url = _config.base_URL_no_path + rjson['links']['next']
    else:
      break

  return xm_people

def get_devices_by_person(person_id):
  """Gets a person's device(s)

  Parameters:
    ID (targetName or id)

  Returns:
    {
      "count":3,
      "total":3,
      "data":[
      {
        "id":"a4d69579-f436-4e85-9d93-703714d85d72",
        "name":"Home Phone",
        "recipientType":"DEVICE",
        "phoneNumber":"+13235553643",
        "targetName":"akaur",
        "deviceType":"VOICE",
    [...]
  """

  print_debug(3, "\n")
  print_debug(1, "Gathering all devices for %s" % person_id)
  url = _config.base_URL + '/people/' + person_id + '/devices'

  headers = {'Authorization': 'Bearer ' + get_access_token()}

  xm_devices = []
  while True:
    response = requests.get(url, headers=headers, proxies=_config.proxies)

    if (response.status_code == 200):
      rjson = response.json()
      print_debug(2, 'Retrieved ' + str(rjson['count']) + ' of ' + str(rjson['total']) + " devices.")
    else:
      print(response)
      raise Exception(response.content)
  
    for device in rjson['data']:
      print_debug(4, "Device - %s %s" % (device['name'],device['targetName']))
      xm_devices.append(device)

    if 'next' in rjson['links']:
      url = _config.base_URL_no_path + rjson['links']['next']
    else:
      break

  return xm_devices

def add_work_email_device(xm_user):
  print_debug(3, "\n")
  print_debug(1, "Adding device %s to XMatters" % (xm_user['targetName']))
  url = _config.base_URL + '/devices'

  headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + get_access_token() }

  if not re.search('@', xm_user['targetName']):
    print_debug(1, "NOT adding device for %s because that ain't no email address!" % xm_user['targetName'])
    return

  device_data = {
    'recipientType': 'DEVICE',
    'deviceType' : 'EMAIL',
    'owner': xm_user['id'],
    'name': 'Work Email',
    'emailAddress': xm_user['targetName'],
    'delay' : 0,
    'priorityThreshold': 'MEDIUM',
    'testStatus' : 'UNTESTED',
  }

  response = requests.post(url, headers=headers, data=json.dumps(device_data), proxies=_config.proxies)

  if (response.status_code == 201):
    rjson = response.json()
  else:
    print("ERROR: something went wrong adding device for user %s" % (xm_user['targetName']))
    print(response)
    print(response.content)
    raise Exception(response.content)





# THIS IS A URL TO POST ALERTS TO XMATTERS IF YOU WANT TO DO THAT
#https://mozilla-np.xmatters.com/api/integration/1/functions/33853389-18a6-419a-891f-8b367e0c7209/triggers?apiKey=f0f6ebf0-082c-49da-8be0-52d770fdc168

# add site to xmatters
# OLD API
# https://help.xmatters.com/OnDemand/xmodwelcome/communicationplanbuilder/appendixrestapi.htm?cshid=apiGETsites#GETsites
#
def add_site(site):
  print_debug(3, "\n")
  print_debug(1, "Adding site %s to XMatters" % site)

  # fixup bad data
  if site['country'] == 'United States of America':
    site['country'] = 'United States'
  elif site['country'] == 'Vietnam':
    site['country'] = 'Viet Nam'
  if site['postal_code'] == 'CZECH REPUBLIC':
    site['postal_code'] = ''

  site_data = {
    'name':       site['name'],
    'timezone':   site['timezone'],
    # skip address for now as it's mostly bad data (remote sites)
    #'address1':   site['address'],
    'country':    site['country'],
    'city':       site['city'],
    'state':      site['state'],
    'postalCode': site['postal_code'],
    'status':   'ACTIVE',
  }
  sites_url = _config.base_URL_old_api + 'sites'

  headers = {'Content-Type': 'application/json'}

  response =  requests.post(sites_url, auth=(_config.xm_username,_config.xm_password), headers=headers, data=json.dumps(site_data), proxies=_config.proxies)
  if (response.status_code == 200):
    rjson = response.json();
    print_debug(1, rjson)
  else:
    print('Could not create site')
    print(response.content)
    raise Exception(response.content)

# OLD API
# https://help.xmatters.com/OnDemand/xmodwelcome/communicationplanbuilder/appendixrestapi.htm?cshid=apiGETsites#GETsites
#
def set_site_inactive(xm_site_id):
  print_debug(1, "Setting site %s to inactive" % xm_site_id)

  site_data = {
    'status': 'INACTIVE',
  }
  sites_url = _config.base_URL_old_api + 'sites/' + xm_site_id

  headers = {'Content-Type': 'application/json'}

  response =  requests.post(sites_url, auth=(_config.xm_username,_config.xm_password), headers=headers, data=json.dumps(site_data), proxies=_config.proxies)
  if (response.status_code == 200):
    rjson = response.json();
    print_debug(1, rjson)
  else:
    print('Could not deactivate site')
    print(response.content)
    raise Exception(response.content)

def add_new_sites(wd_sites,xm_sites):
  print_debug(3, "\n")
  print_debug(1, "Adding new sites to XMatters")
  xm_sites_in_wd = {}
  for wd_site in wd_sites:
    if wd_site in xm_sites:
      print_debug(3, "WD site %s found in XMatters! No action." % wd_site)
      xm_sites_in_wd[ wd_site ] = 1
    else:
      print_debug(1, "WD site %s NOT found in XMatters! Adding to XMatters." % wd_site)
      add_site(wd_sites[wd_site])


  return xm_sites_in_wd

def delete_sites(xm_sites,xm_sites_in_wd):
  print_debug(3, "\n")
  print_debug(1, "Deleting empty sites from XMatters")
  for site in xm_sites:
    if site not in xm_sites_in_wd:
      print_debug(1, "Site %s not in WorkDay. INACTIVATING %s from XMatters" % (site,xm_sites[site]))
      set_site_inactive(xm_sites[site])

# NEW API
# https://help.xmatters.com/xmAPI/?python#modify-a-person
#
def update_user(wd_user,xm_user,xm_sites):
  print_debug(1, "Updating user %s (%s) in XMatters" % (xm_user['id'],xm_user['targetName']))
  url = _config.base_URL + '/people'

  headers = { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + get_access_token() }

  manager_name = ''
  if 'Worker_s_Manager' in wd_user:
    manager_name = wd_user['Worker_s_Manager'][0]['User_Manager_Preferred_First_Name'] + ' ' \
                   + wd_user['Worker_s_Manager'][0]['User_Manager_Preferred_Last_Name']
  person_data = {
    'id':        xm_user['id'],
    'firstName': wd_user['User_Preferred_First_Name'],
    'lastName':  wd_user['User_Preferred_Last_Name'],
    'site':      xm_sites[ wd_user['User_Work_Location'] ],
    'properties': {
      'Cost Center':      wd_user['User_Cost_Center'],
      'Manager':          manager_name,
      'Manager Email':    wd_user.get('User_Manager_Email_Address',''),
      'Functional Group': wd_user.get('User_Functional_Group',''),
      'Home City':        wd_user.get('User_Home_City',''),
      'Home Country':     wd_user.get('User_Home_Country',''),
      'Home Zipcode':     wd_user.get('User_Home_Postal_Code',''),
    }
  }
 
  print_debug(3, "will upload this:")
  print_debug(3, json.dumps(person_data))

  response = requests.post(url, headers=headers, data=json.dumps(person_data), proxies=_config.proxies)

  if (response.status_code == 200):
    rjson = response.json()
  else:
    print("ERROR: something went wrong updating user %s (%s)" % (xm_user['id'],xm_user['targetName']))
    print(response)
    raise Exception(response.content)

# NEW API
# https://help.xmatters.com/xmAPI/?python#create-a-person
#
def add_user(wd_user,xm_sites):
  print_debug(3, "\n")
  print_debug(1, "Adding user %s to XMatters" % (wd_user['User_Email_Address']))
  url = _config.base_URL + '/people'

  headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + get_access_token() }

  manager_name = ''
  if 'Worker_s_Manager' in wd_user:
    manager_name = wd_user['Worker_s_Manager'][0]['User_Manager_Preferred_First_Name'] + ' ' \
                   + wd_user['Worker_s_Manager'][0]['User_Manager_Preferred_Last_Name']
  person_data = {
    'firstName':      wd_user['User_Preferred_First_Name'],
    'lastName':       wd_user['User_Preferred_Last_Name'],
    'targetName':     wd_user['User_Email_Address'],
    'site':           xm_sites[ wd_user['User_Work_Location'] ],
    'recipientType': 'PERSON',
    'status':        'ACTIVE',
    'roles':         ['Standard User'],
    'supervisors':   [_config.supervisor_id],
    'properties': {
      'Cost Center':      wd_user['User_Cost_Center'],
      'Manager':          manager_name,
      'Manager Email':    wd_user.get('User_Manager_Email_Address',''),
      'Functional Group': wd_user.get('User_Functional_Group',''),
      'Home City':        wd_user.get('User_Home_City',''),
      'Home Country':     wd_user.get('User_Home_Country',''),
      'Home Zipcode':     wd_user.get('User_Home_Postal_Code',''),
    }
  }
 
  print_debug(3, "will upload this:")
  print_debug(3, json.dumps(person_data))

  response = requests.post(url, headers=headers, data=json.dumps(person_data), proxies=_config.proxies)

  if (response.status_code == 201):
    rjson = response.json()
  else:
    print("ERROR: something went wrong adding user %s" % (wd_user['User_Email_Address']))
    print(response)
    print(response.content)
    raise Exception(response.content)

  person_data['id'] = rjson['id']
  add_work_email_device(person_data)

# NEW API
# https://help.xmatters.com/xmAPI/?python#delete-a-person
#
def actual_person_delete(target):
  print_debug(1, "Sending DELETE request for %s" % target)

  url = _config.base_URL + '/people/' + target
 
  headers = {'Authorization': 'Bearer ' +  get_access_token() }

  response = requests.delete(url, headers=headers, proxies=_config.proxies)

  if (response.status_code == 200):
    print_debug(1, 'Deleted person ' +  response.json().get('targetName'))
  elif (response.status_code == 204):
    print_debug(1, 'The person could not be found.')
  else:
    print('Could not delete person!')
    print(response)
    print(response.content)
    raise Exception(response.content)

def delete_users(xm_users,users_seen_in_wd):
  print_debug(3, "\n")
  print_debug(1, "Deleting old users from XMatters")
  for user in xm_users:
    if not re.search('@',user):
      # let's just skip any usernames that don't look like emails
      continue
    if user not in users_seen_in_wd:
      print_debug(1, "User %s not seen in workday, will delete from xmatters" % user)
      actual_person_delete(user)
