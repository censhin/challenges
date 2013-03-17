#!/usr/bin/env python

import pyrax
import time

pyrax.set_credential_file("/home/graft/.rackspace_cloud_credentials")
cs = pyrax.cloudservers
ubu_image = [img for img in cs.images.list()
    if "Ubuntu 12.04" in img.name][0]
flavor_512 = [flavor for flavor in cs.flavors.list()
    if flavor.ram == 512][0]
server_list = []

for i in range(1, 4):
    server = cs.servers.create("server%d"%i, ubu_image.id, flavor_512.id)
    server_list.append(server)

time.sleep(60)

for n in server_list:
    print n
    if len(n.networks['public'][0]) <= 15:
        print "IP Address: %s" % n.networks['public'][0]
    else:
        print "IP Address: %s" % n.networks['public'][1]
    print "Password: %s" % n.adminPass
