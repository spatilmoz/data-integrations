import os

__location__ = os.path.realpath(os.path.dirname(__file__))
script_dir = os.path.dirname(__file__)
rel_path = 'dp2-dev-fdeb93967c4d.json'
gcp_public_key_file_path = os.path.join(__location__, os.path.join(script_dir, rel_path))

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