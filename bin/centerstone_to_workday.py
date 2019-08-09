#!/usr/bin/env python3

from __future__ import division
import sys,os, argparse
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from integrations.connectors import Centerstone, Workday, Util


def compare_seats(wd_seats,cs_seats):
  logger.info( "Comparing Workday seats to Centerstone...")

  errors_not_in_wd = []
  errors_not_in_cs = []

  for wd_emp in wd_seats:
    if wd_emp not in cs_seats:
      errors_not_in_cs.append("[ERROR] Employee ID %s not found in Centerstone data" % wd_emp)
    elif wd_seats[wd_emp] != cs_seats[wd_emp]:
      logger.warning( "Employee ID %s has seat %s in Centerstone and %s in Workday" % (wd_emp,cs_seats[wd_emp],wd_seats[wd_emp]))

  for cs_emp in cs_seats:
    if cs_emp not in wd_seats:
      errors_not_in_wd.append("[ERROR] Employee ID %s not found in Workday data" % cs_emp)

  for error in errors_not_in_wd:
    logger.error(error)
  for error in errors_not_in_cs:
    logger.error(error)

if __name__ == "__main__":
 
  parser = argparse.ArgumentParser(description="Sync up XMatters with Workday")
  parser.add_argument('-d', '--debug', action='store', help='debug level', type=int, default=3)
  parser.add_argument('-l', '--log-level', action='store', help='log level (debug, info, warning, error, or critical)', type=str, default='info')
  parser.add_argument('-f', '--force', action='store_true', help='force changes even if there are a lot')
  args = parser.parse_args()

  Util.set_up_logging(args.log_level)

  logger = logging.getLogger(__name__)

  logger.info("Starting...")

  # get all sites in xmatters
  cs_seats = Centerstone.get_all_seats()

  # get all users from workday
  wd_seats = Workday.get_seating()

  compare_seats(wd_seats,cs_seats)
