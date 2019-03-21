# data-integrations

## XMatters.py
TODO: More documentation

Two APIs for XMatters as of this writing (20180214). The old one:

https://help.xmatters.com/OnDemand/xmodwelcome/communicationplanbuilder/appendixrestapi.htm

which is for sites, and the new one:

https://help.xmatters.com/xmAPI/?python

which is for OAuth, People, and the rest.

Expects a config file called `secrets_xmatters.py` which looks like this:
```
config = {
  'proxies'      : {},
  'xm_client_id' : 'CLIENT-ID-HERE',
  'xm_username'  : 'USERNAMEHERE',
  'xm_password'  : 'PASSWORDHERE',
}
```

## Workday.py
Expects a config file called `secrets_workday.py` which looks like this:
```
config = {
  'proxies'               : {},
  'xmatters_integration' : {
    'username'   : 'USERNAME',
    'password'   : 'PASSWORD',
    'sites_url'  : 'https://example',
    'people_url' : 'https://example1',
  },
  'seating' : {
    'username': 'USERNAME2',
    'password': 'PASSWORD2',
    'url'     : 'https://example2',
  },
  'hr_dashboard' : {
    'username': 'USERNAME3',
    'password': 'PASSWORD3',
    'urls': {
      'headcount': 'https://example4',
      'hires': 'https://example5',
      'terminations': 'https://example6',
      'promotions': 'https://example7',
    },
  },
}
```

## BrickFTP.py
For interacting with BrickFTP's API.

Expects a config file called `secrets_brickftp.py` which looks like this:
```
config = {
  'proxies'  : {},
  'api_key'  : 'putyourapikeyhere',
  'username' : 'username',   # not used, just including FYI
}
```

