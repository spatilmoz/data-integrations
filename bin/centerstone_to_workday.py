#!/usr/bin/env python3

from __future__ import division
import time
import requests
import json,sys,os,errno,re,argparse
from datetime import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import Centerstone
import Workday

parser = argparse.ArgumentParser(description="Sync up XMatters with Workday")
parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
parser.add_argument('-f', '--force', action='store_true', help='force changes even if there are a lot')
args = parser.parse_args()

debug = args.debug

def print_debug(level, message):
  if debug >= level:
    print("[%s] %s" % (datetime.now(),message))

def compare_seats(wd_seats,cs_seats):
  print_debug(1, "Comparing Workday seats to Centerstone...")
  print_debug(3, '')

  errors_not_in_wd = []
  errors_not_in_cs = []

  for wd_emp in wd_seats:
    if wd_emp not in cs_seats:
      errors_not_in_cs.append("[ERROR] Employee ID %s not found in Centerstone data" % wd_emp)
    elif wd_seats[wd_emp] != cs_seats[wd_emp]:
      print_debug(1, "Employee ID %s has seat %s in Centerstone and %s in Workday" % (wd_emp,cs_seats[wd_emp],wd_seats[wd_emp]))

  for cs_emp in cs_seats:
    if cs_emp not in wd_seats:
      errors_not_in_wd.append("[ERROR] Employee ID %s not found in Workday data" % cs_emp)

  for error in errors_not_in_wd:
    print_debug(1, error)
  for error in errors_not_in_cs:
    print_debug(1, error)

if __name__ == "__main__":
 
  print_debug(1, "Starting...")

  Centerstone.debug(debug)
  Workday.debug(debug)

  # get all sites in xmatters
  cs_seats = Centerstone.get_all_seats()

  # get all users from workday
  wd_seats = Workday.get_seating()

  compare_seats(wd_seats,cs_seats)
