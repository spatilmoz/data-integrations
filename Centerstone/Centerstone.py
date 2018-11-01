import time
#import requests
import json,sys,os,errno,re
from secrets_centerstone import config as cs_config
from datetime import datetime
from subprocess import call
import logging

logger = logging.getLogger(__name__)

class LocalConfig(object):
  def __init__(self):
    self.locations_to_codes = {
      'San Francisco':  'SF',
      'Mountain View':  'MV',
      'Portland':      'PDX',
      'London':        'LON',
      'Vancouver':     'YVR',
      'Toronto':       'TOR',
      'Paris':         'PAR',
      'Berlin':        'BER',
      'Auckland':      'AKL',
      'Beijing':        'BJ',
      'Taipei':        'TPE',
      'Off-Site':         '',
      'Pocket':           '',
    }

  def __getattr__(self, attr):
    return cs_config[attr]

_config = LocalConfig()

def get_seating_data():
  # This happens from the AWS boomi box - maybe a cert there? or limited by IP?
  call(['sftp','-i','secrets_id_rsa.for_centerstone_data','MozillaBrickFTP@ftp.asset-fm.com:/Out/HrExport.txt','/tmp/HrExport.txt'])
  return '/tmp/HrExport.txt'

def load_seating_data(filename='/tmp/HrExport.txt'):
  f = open(filename,'r')
  seating = {}
  for line in f:
    (emp_id,office,office_key,trash,seat_id) = line.split("\t")
    seat_id = seat_id.rstrip()
    #print "%s -- %s" % (emp_id,_config.locations_to_codes[office_key]+seat_id)
    if seat_id == '':
      seating[emp_id] = ''
    else:
      seating[emp_id] = _config.locations_to_codes[office_key]+seat_id
  return seating

def get_all_seats():
  filename = get_seating_data()
  return load_seating_data(filename)


if __name__ == "__main__":
  load_seating_data()
