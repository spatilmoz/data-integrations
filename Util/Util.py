import time
import requests
import json,sys,os,errno,re
from datetime import datetime
from .secrets_util import config as util_config

class LocalConfig(object):
  def __init__(self):
    pass
    
  def __getattr__(self, attr):
    return util_config[attr]

_config = LocalConfig()

def debug(debug=None):
  if debug == None:
    return _config.debug
  else:
    _config.debug = debug

def print_debug(level, message):
  if _config.debug >= level:
    print("[%s] %s" % (datetime.now(),message))
  
def postal_to_coords_and_timezone(loc):
  from .classes.mozgeo import MozGeo
  geo = MozGeo(_config)
  coords = geo.postal_to_coords(loc)
  if coords != (None, None):
    tz = geo.coords_to_timezone(coords)
  else:
    tz = None
  return(coords, tz)
