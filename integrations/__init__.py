import os

try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'integrations/api/config/google_secrets.json'
except:
    pass