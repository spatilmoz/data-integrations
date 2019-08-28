import os


config = {
  'proxies': {},
  'MozGeo': {
    'google_api_key' : os.environ.get('MOZGEO_GOOGLE_API_KEY',''),
  },
  'storage': {
    'bucket': os.environ.get('BUCKET', ''),
    'dataset': os.environ.get('DATASET', ''),
    'google_application_credentials': os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''),
  },
  'gpg' : {
    'public_key': os.environ.get('PUBLIC_KEY', ''),
    'public_key_test': os.environ.get('PUBLIC_KEY_TEST', ''),
    'key_id':  os.environ.get('KEY_ID', ''),
    'key_id_test': os.environ.get('KEY_ID_TEST', ''),
    'private_key': os.environ.get('PRIVATE_KEY', ''),
    'private_key_test': os.environ.get('PRIVATE_KEY_TEST', ''),
    'encrypted_dir': os.environ.get('ENCRYPTED_DIR', '')
  },
  'sftp': {
    'host': os.environ.get('HOST', ''),
    'username': os.environ.get('USERNAME', ''),
    'password': os.environ.get('PASSWORD', ''),
    'sftp_dir': os.environ.get('SFTP_DIR', '')
  }
}