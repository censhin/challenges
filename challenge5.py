#!/usr/bin/env python

import sys
import time
import pyrax

def get_instance(inst_name):
    inst = [inst for inst in cdb.list()
            if inst_name in inst.name][0]
    time.sleep(5)
    return inst

pyrax.set_credential_file("/home/graft/.rackspace_cloud_credentials")
cdb = pyrax.cloud_databases
flavors = cdb.list_flavors()

f_ram = int(raw_input("Select the database instance size %s: "
    % [f.ram for f in flavors]))
volume = int(raw_input("Enter disk space in GB: "))
inst_name = raw_input("Enter the instance's name: ")
db_name = raw_input("Enter the database's name: ")
user_name = raw_input("Enter the user's name: ")
password = raw_input("Enter the user's password: ")

flavor = [f for f in flavors if f_ram == f.ram][0]
instance = cdb.create(inst_name, flavor=flavor.name, volume=volume)

while True:
    sys.stdout.flush()
    inst = get_instance(instance.name)
    if inst.status != 'ACTIVE':
        sys.stdout.write("Status: %s\r" % inst.status)
    else:
        print "Status: %s" % inst.status
        print "Creating the database and user."
        break

db = instance.create_database(db_name)
user = instance.create_user(name=user_name, password=password, database_names=[db])
