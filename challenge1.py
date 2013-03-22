#!/usr/bin/env python
"""
<--Challenge 1-->
Write a script that builds three 512 MB Cloud Servers that
following a similar naming convention. (ie., web1, web2, web3)
and returns the IP and login credentials for each server.
Use any image you want.

@author: Neill Johnson
@date: March 14, 2013
"""

import os
import pyrax
import time

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

# choose Ubuntu 12.04 image
ubu_image = [img for img in cs.images.list()
            if "Ubuntu 12.04" in img.name][0]

# choose size of servers to be 512Mb
flavor_512 = [flavor for flavor in cs.flavors.list()
            if flavor.ram == 512][0]

server_list = []

# create three servers
for i in range(1, 4):
    server = cs.servers.create("server%d"%i, ubu_image.id, flavor_512.id)
    server_list.append(server)

# wait for networking info to propagate
time.sleep(60)

# print server info
for n in server_list:
    print n
    if len(n.networks['public'][0]) <= 15:
        print "IP Address: %s" % n.networks['public'][0]
    else:
        print "IP Address: %s" % n.networks['public'][1]
    print "Password: %s" % n.adminPass
