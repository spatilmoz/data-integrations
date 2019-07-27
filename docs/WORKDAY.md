# Workday

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