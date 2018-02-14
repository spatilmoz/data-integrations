import requests
import json,sys,os,errno,re
from secret import config
from datetime import datetime

debug = 3

proxies = {"https" : "http://proxy.dmz.scl3.mozilla.com:3128"}

base_URL         = 'https://mozilla-np.xmatters.com/api/xm/1'
base_URL_old_api = 'https://mozilla-np.xmatters.com/reapi/2015-04-01/'

access_token = False

def print_debug(level, message):
  if debug >= level:
    print "[%s] %s" % (datetime.now(),message)

def get_access_token():
  global access_token
  if not access_token:
    access_token = _get_access_token()
  return access_token

def _get_access_token():
  endpoint_URL = '/oauth2/token' 
  grant_type='password'
  url = base_URL + endpoint_URL +'?grant_type='+grant_type+'&client_id='+config['xm_client_id']+'&username='+config['xm_username']+'&password='+config['xm_password']

  headers = {'Content-Type': 'application/json'}

  response = requests.post(url, headers=headers)

  if (response.status_code == 200):
     rjson = response.json();
     print_debug(5, 'Access token: ' + rjson.get('access_token') + ', \nRefresh token: ' + rjson.get('refresh_token'))
     access_token = rjson.get('access_token')
  else:
     error = 'Could not get an access token'
     print error
     raise Exception(error)

  return access_token

# get all xmatters sites
# OLD API
# https://help.xmatters.com/OnDemand/xmodwelcome/communicationplanbuilder/appendixrestapi.htm?cshid=apiGETsites#GETsites
#
def get_all_sites():
  print_debug(3, "\n")
  print_debug(1, "Gathering all XMatters sites")
  all_sites_url = base_URL_old_api + 'sites'
  response =  requests.get(all_sites_url, auth=(config['xm_username'],config['xm_password']))
  if (response.status_code == 200):
    rjson = response.json();
    print_debug(5, rjson)
  else:
    error = 'Could not get sites'
    print error
    raise Exception(error)
  
  xm_sites = {}
  for site in rjson['sites']:
    print_debug(3, site['name']+' -- '+site['identifier'])
    print_debug(5, site)
    if site['status'] == 'ACTIVE':
      xm_sites[ site['name'] ] = site['identifier']
    else:
      print_debug(2, "Skipping XMatters site %s because status is %s" % (site['name'],site['status']))

  return xm_sites

# get all people from xmatters
# NEW API
# https://help.xmatters.com/xmAPI/?python#get-people
#
def get_all_people():
  print_debug(3, "\n")
  print_debug(1, "Gathering all XMatters people")
  url = base_URL + '/people'

  headers = {'Authorization': 'Bearer ' + get_access_token()}

  response = requests.get(url, headers=headers)

  if (response.status_code == 200):
    rjson = response.json()
    print_debug(2, 'Retrieved ' + str(rjson['count']) + ' of ' + str(rjson['total']) + " people.")
  else:
    print response
    raise Exception(response.content)

  xm_people = {}
  for person in rjson['data']:
    print_debug(2, "%s %s (%s)" % (person['firstName'],person['lastName'],person['targetName']))
    if person['lastName'] == 'Valaas':
      print_debug(2, person)
    xm_people[ person['targetName'] ] = person

  return xm_people

# add site to xmatters
# OLD API
# https://help.xmatters.com/OnDemand/xmodwelcome/communicationplanbuilder/appendixrestapi.htm?cshid=apiGETsites#GETsites
#
def add_site(site):
  print_debug(3, "\n")
  print_debug(1, "Adding site %s to XMatters" % site)

  site_data = {
    'name':   site,
    'status': 'ACTIVE',
  }
  sites_url = base_URL_old_api + 'sites'

  headers = {'Content-Type': 'application/json'}

  response =  requests.post(sites_url, auth=(config['xm_username'],config['xm_password']), headers=headers, data=json.dumps(site_data))
  if (response.status_code == 200):
    rjson = response.json();
    print_debug(1, rjson)
  else:
    print ('Could not create site')
    print response.content
    raise Exception(response.content)

# OLD API
# https://help.xmatters.com/OnDemand/xmodwelcome/communicationplanbuilder/appendixrestapi.htm?cshid=apiGETsites#GETsites
#
def set_site_inactive(xm_site_id):
  print_debug(1, "Setting site %s to inactive" % xm_site_id)

  site_data = {
    'status': 'INACTIVE',
  }
  sites_url = base_URL_old_api + 'sites/' + xm_site_id

  headers = {'Content-Type': 'application/json'}

  response =  requests.post(sites_url, auth=(config['xm_username'],config['xm_password']), headers=headers, data=json.dumps(site_data))
  if (response.status_code == 200):
    rjson = response.json();
    print_debug(1, rjson)
  else:
    print ('Could not deactivate site')
    print response.content
    raise Exception(response.content)

def add_new_sites(wd_sites,xm_sites):
  print_debug(3, "\n")
  print_debug(1, "Adding new sites to XMatters")
  xm_sites_in_wd = {}
  for wd_site in wd_sites:
    if wd_site in xm_sites:
      print_debug(5, "WD site %s found in XMatters! No action." % wd_site)
      xm_sites_in_wd[ wd_site ] = 1
    else:
      print_debug(1, "WD site %s NOT found in XMatters! Adding to XMatters." % wd_site)
      add_site(wd_site)

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
  url = base_URL + '/people'

  headers = { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + get_access_token() }

  person_data = {
    'id':        xm_user['id'],
    'firstName': wd_user['First_Name'],
    'lastName':  wd_user['Last_Name'],
    'site':      xm_sites[ wd_user['Location'] ],
    'properties': {
      'Cost Center':      wd_user['Cost_Center'],
      'Manager':          wd_user['Manager_Name'],
      'Functional Group': wd_user['Functional_Group'],
    }
  }
 
  print_debug(3, "will upload this:")
  print_debug(3, json.dumps(person_data))

  response = requests.post(url, headers=headers, data=json.dumps(person_data))

  if (response.status_code == 200):
    rjson = response.json()
  else:
    print "ERROR: something went wrong updating user %s (%s)" % (xm_user['id'],xm_user['targetName'])
    print response
    raise Exception(response.content)

# NEW API
# https://help.xmatters.com/xmAPI/?python#create-a-person
#
def add_user(wd_user,xm_sites):
  return
  print_debug(3, "\n")
  print_debug(1, "Adding user %s to XMatters" % (wd_user['Email_Address']))
  url = base_URL + '/people'

  headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + get_access_token() }

  person_data = {
    'firstName':      wd_user['First_Name'],
    'lastName':       wd_user['Last_Name'],
    'targetName':     wd_user['Email_Address'],
    'site':           xm_sites[ wd_user['Location'] ],
    'recipientType': 'PERSON',
    'status':        'ACTIVE',
    'roles':         ['Standard User'],
    'properties': {
      'Cost Center':      wd_user['Cost_Center'],
      'Manager':          wd_user['Manager_Name'],
      'Functional Group': wd_user['Functional_Group'],
    }
  }
 
  print_debug(3, "will upload this:")
  print_debug(3, json.dumps(person_data))

  response = requests.post(url, headers=headers, data=json.dumps(person_data))

  if (response.status_code == 201):
    rjson = response.json()
  else:
    print "ERROR: something went wrong adding user %s" % (wd_user['Email_Address'])
    print response
    print response.content
    raise Exception(response.content)

# NEW API
# https://help.xmatters.com/xmAPI/?python#delete-a-person
#
def actual_person_delete(target):
  print_debug(1, "Sending DELETE request for %s" % target)

  url = base_URL + '/people/' + target
 
  headers = {'Authorization': 'Bearer ' +  get_access_token() }

  response = requests.delete(url, headers=headers)

  if (response.status_code == 200):
    print_debug(1, 'Deleted person ' +  response.json().get('targetName'))
  elif (response.status_code == 204):
    print_debug(1, 'The person could not be found.')
  else:
    print 'Could not delete person!'
    print response
    print response.content
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
