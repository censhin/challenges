#!/usr/bin/env python

import sys
import pyrax

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
inst = [inst for inst in cdb.list()
        if inst_name in inst.name][0]

print "Waiting for the image to finish building."
pyrax.utils.wait_until(inst, "status", ['ACTIVE', 'ERROR'], interval=20, attempts=40, verbose=True)
print "\nCreating the database and user."
db = instance.create_database(db_name)
user = instance.create_user(name=user_name, password=password, database_names=[db])
