#!/usr/bin/env python

import sys
import pyrax
import time
from pyrax import utils

pyrax.set_credential_file("/home/graft/.rackspace_cloud_credentials")
cs = pyrax.cloudservers
server = cs.servers.list()
flavor = server[0].flavor['id']
server[0].create_image("backup_image")
clone_image = [img for img in cs.images.list()
        if img_name in img.name][0]

print "Waiting for image to finish building."
utils.wait_until(clone_image, "status", ['ACTIVE', 'ERROR'], interval=20, attempts=40, verbose=True)
print "Creating server from image."
clone = cs.servers.create("clone", clone_image.id, flavor)
