import os

try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/var/secrets/google/key.json'
except:
    pass