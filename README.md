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
  'proxies'              : {},
  'wd_username'          : 'FIRSTUSERNAMEHERE',
  'wd_password'          : 'FIRSTPASSWORDHERE',
  'wd_seating_username'  : 'SECONDUSERNAME',
  'wd_seating_password'  : 'SECONDPASSWORD',
}
```

## BrickFTP.py
For interacting with BrickFTP's API.

Expects a config file called `secrets_brickftp.py` which looks like this:
```
config = {
  'api_key'  : 'putyourapikeyhere',
  'username' : 'username',   # not used, just including FYI
}
```
