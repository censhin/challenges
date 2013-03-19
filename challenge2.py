#!/usr/bin/env python

import os
import sys
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
server = cs.servers.list()
flavor = server[0].flavor['id']
img_name = raw_input("Input the image name: ")
serv_name = raw_input("Input the server name: ")
server[0].create_image(img_name)
clone_image = [img for img in cs.images.list()
        if img_name in img.name][0]

print "Waiting for image to finish building."
pyrax.utils.wait_until(clone_image, "status", ['ACTIVE', 'ERROR'], interval=20, attempts=40, verbose=True)
print "\nCreating server from image."
clone = cs.servers.create(serv_name, clone_image.id, flavor)
