import os
config = {
  'proxies'  : {},
  'api_key'  : os.environ.get('BRICKFTP_API_KEY',''),
  'username' : 'sfmc-etl',   # not used, just including FYI
}
