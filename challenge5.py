#!/usr/bin/env python
"""
<--Challenge 5-->
Write a script that creates a Cloud Database instance. This
instance should contain at least one database, and the database
should have at least one user that can connect to it.

@author: Neill Johnson
@date: March 17, 2013
"""

import os
import sys
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cdb = pyrax.cloud_databases
flavors = cdb.list_flavors()

# prompt the user for DB info to create the DB and user
f_ram = int(raw_input("Select the database instance size %s: "
    % [f.ram for f in flavors]))
volume = int(raw_input("Enter disk space in GB: "))
inst_name = raw_input("Enter the instance's name: ")
db_name = raw_input("Enter the database's name: ")
user_name = raw_input("Enter the user's name: ")
password = raw_input("Enter the user's password: ")

"""
select the flavor, create the DB, and store the
DB instance
"""
flavor = [f for f in flavors if f_ram == f.ram][0]
instance = cdb.create(inst_name, flavor=flavor.name, volume=volume)
inst = [inst for inst in cdb.list()
        if inst_name in inst.name][0]

print "Waiting for the image to finish building."
pyrax.utils.wait_until(inst, "status", ['ACTIVE', 'ERROR'], interval=20, attempts=40, verbose=True)

print "\nCreating the database and user."
db = instance.create_database(db_name)
user = instance.create_user(name=user_name, password=password, database_names=[db])
