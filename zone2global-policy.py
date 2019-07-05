#!/usr/bin/env python3

#Converts/Migrates a zone based policy to global policy in Juniper SRX
#
#Author: Genco Y. <genco{AT}rto{DOT}net>

import sys


if len(sys.argv) < 2:
  print("Usage: \n" + sys.argv[0] + " {zone based policy in set format} " )
  sys.exit()


zone_based_policy_file = sys.argv[1]

with open(zone_based_policy_file,'r') as zone_policy:
  uniq_line = "none"
  for set_zone_command in zone_policy:
    if set_zone_command.startswith('set'):
      set_line = set_zone_command.split()
      uniq_line_tmp = "".join(set_line[:9])
      from_zone = set_line[4]
      to_zone = set_line[6]
      orig_policy_name = set_line[8]
      rest_of_set_line = " ".join(set_line[9:])
      if (uniq_line_tmp != uniq_line):
        #add source/destination zones to policy
        print("set security policies global policy " + from_zone + "-" + to_zone + "-" + orig_policy_name + " " + "match from-zone " + from_zone  )
        print("set security policies global policy " + from_zone + "-" + to_zone + "-" + orig_policy_name + " " + "match to-zone " + to_zone  )

      #Print what we convert from the policy
      print("set security policies global policy " + from_zone + "-" + to_zone + "-" + orig_policy_name + " " + rest_of_set_line )
      uniq_line = uniq_line_tmp

