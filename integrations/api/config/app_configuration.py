import os

config = {
  'proxies': {},
  'MozGeo': {
    'google_api_key' : os.environ.get('MOZGEO_GOOGLE_API_KEY',''),
  },
  'gpg' : {
    'gpg_public_key_url': os.environ.get('PUBLIC_KEY_URL',
                                     'https://members.exacttarget.com/Content/Subscribers/SubsLists/publickey.txt'),
  },
  'sftp': {
    'sftp_host': os.environ.get('SFTP_HOST', ''),
    'sftp_username': os.environ.get('SFTP_USERNAME', ''),
    'sftp_password': os.environ.get('SFTP_PASSWORD', '')
  }
}