import os
config = {
  "type": "service_account",
  "project_id": os.environ.get('PROJECT_ID',''),
  "private_key_id": os.environ.get('PRIVATE_KEY_ID',''),
  "private_key": os.environ.get('PRIVATE_KEY',''),
  "client_email": os.environ.get('CLIENT_EMAIL',''),
  "client_id": os.environ.get('CLIENT_ID',''),
  "auth_uri": os.environ.get('AUTH_URI',''),
  "token_uri": os.environ.get('TOKEN_URI',''),
  "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_CERT',''),
  "client_x509_cert_url": os.environ.get('CLIENT_CERT_URL',''),
}

