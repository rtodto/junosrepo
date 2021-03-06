#!/usr/bin/env python3

#Description: Converts an Juniper SRX address book file in zone based set 
#             format to global address book
#Note: 
# - Junos address book names are case sensitive
# Global format: set security address-book global address <address-object-name> 
# Zone based format: 
#Address object: set security zones security-zone <zonename> address-book address <address-object-name> <IPaddress>
#                set security zones security-zone <zonename> address-book address dns-name <FQDN>
#                set security zones security-zone <zonename> address-book address description <description>
#Address set: set security zones security-zone <zonename> address-book address-set <address-set-name> address <address-object-name>
#Address set: set security zones security-zone <zonename> address-book address-set <address-set-name> address-set <address-set-name>

import sys
import shlex

arg_len = len(sys.argv)
if arg_len < 2:
  print('{} AddressFile\n'.format(sys.argv[0]))
  print('AddressFile: in set based security zone based format ')

  sys.exit()

addressbook_file=sys.argv[1]

address_list = {}
duplicate_address_list = []
address_set_list = []
zone_names = []
with open(addressbook_file,'r') as address_f:
  for addr_object in address_f:
    if addr_object.startswith('set'):
      addr_object_sep = shlex.split(addr_object)     
    else:
      continue
    #Collect address objects
    if addr_object_sep[6] == 'address':

      if addr_object_sep[8] == 'description':
        #convert spaces to underscore if there is any 
        description = addr_object_sep[9].replace(" ","_")
        print('set security address-book global address {} description {}'.format(addr_object_sep[7],description))          
      elif addr_object_sep[8] == 'range-address':
        range_address = ' '.join(addr_object_sep[9:])
        print('set security address-book global address {} range-address {}'.format(addr_object_sep[7],range_address))

      elif addr_object_sep[8] == 'wildcard-address':
         print('set security address-book global address {} wildcard-address {}'.format(addr_object_sep[7],addr_object_sep[9]))

      elif addr_object_sep[8] == 'dns-name':
        print('set security address-book global address {} dns-name {}'.format(addr_object_sep[7],addr_object_sep[9])) 

      else: #this is the IP address entry
        if addr_object_sep[7] in address_list: #this is a duplicate address object
          if address_list[addr_object_sep[7]] == addr_object_sep[8]:
            pass #duplicate address object with the same IP value, this is ok 
          else: #this is a duplicate name with a different IP value not acceptable
            duplicate_address_list.append(addr_object_sep[7])

        else: 
          print('set security address-book global address {} {}'.format(addr_object_sep[7],addr_object_sep[8]))
          address_list[addr_object_sep[7]] = addr_object_sep[8]
      zone_names.append(addr_object_sep[4]) #collect zone names

    #Collect address sets
    if addr_object_sep[6] == 'address-set':
      if addr_object_sep[8] == 'address':
        print('set security address-book global address-set {} address {}'.format(addr_object_sep[7],addr_object_sep[9])) 
      elif addr_object_sep[8] == 'address-set': #There can be address-set within address-set
        print('set security address-book global address-set {} address-set {}'.format(addr_object_sep[7],addr_object_sep[9]))

for zone in set(zone_names):
  print('del security zones security-zone {} address-book'.format(zone))


if (len(duplicate_address_list)>0):
  print("\n\nDuplicate address objects found with conflicting object values")
  print("*"*62)
  for dup_address in duplicate_address_list:
    print(dup_address)

  print('\n\n')  


