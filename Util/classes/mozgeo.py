import ssl
import time
import requests
import json,sys,os,errno,re
from datetime import datetime
import geopy.geocoders
from geopy.geocoders import GoogleV3
import Util

class MozGeo(object):
  def __init__(self, config):
    self.config = config.MozGeo

    geopy.geocoders.options.default_proxies = config.proxies
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    geopy.geocoders.options.default_ssl_context = ctx
    self.geolocator = GoogleV3(api_key=self.config['google_api_key'])

  def postal_to_coords(self, location):
    Util.print_debug(5, "postal_to_coords called with %s" % location)
    res = self.geolocator.geocode(components=location)
    if res == None:

      Util.print_debug(1, '')
      Util.print_debug(1, '')
      Util.print_debug(1, '')
      Util.print_debug(1, '')
      Util.print_debug(1, '')
      Util.print_debug(3, "No geolocation found for location %s" % location)
      Util.print_debug(1, '')
      Util.print_debug(1, '')
      Util.print_debug(1, '')
      Util.print_debug(1, '')
      Util.print_debug(1, '')
      return((None, None))
    else:
      Util.print_debug(5, res.raw)
      #print(res)
      #print(res.raw['geometry']['location']['lat'])
      #print(res.raw['geometry']['location']['lng'])
      return((res.raw['geometry']['location']['lat'], res.raw['geometry']['location']['lng']))

  def coords_to_timezone(self, coords):
    Util.print_debug(5, "coords_to_timezone called with %s" % str(coords))
    res = self.geolocator.timezone(coords)
    Util.print_debug(5, res)
    #print(res)
    return res
