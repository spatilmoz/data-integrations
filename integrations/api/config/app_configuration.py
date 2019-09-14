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



bing_revenue_username=os.environ.get('bing_revenue_username')
bing_revenue_password=os.environ.get('bing_revenue_password')
bing_revenue_developer_token=os.environ.get('bing_revenue_developer_token')
bing_revenue_content_type='application/json'