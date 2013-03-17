#!/usr/bin/env python

import sys
import pyrax
import time

def get_image(img_name):
    img = [img for img in cs.images.list()
        if img_name in img.name][0]
    time.sleep(5)
    return img

pyrax.set_credential_file("/home/graft/.rackspace_cloud_credentials")
cs = pyrax.cloudservers
server = cs.servers.list()
flavor = server[0].flavor['id']
server[0].create_image("backup_image")

while True:
    clone_image = get_image("backup_image")
    if clone_image.status != 'ACTIVE':
        sys.stdout.write("Status: %s" % clone_image.status)
    if clone_image.progress != 100:
        sys.stdout.write("Progress: %d%%" % clone_image.progress)
        sys.stdout.flush()
    else:
        print "Creating server from image."
        break

clone = cs.servers.create("clone", clone_image.id, flavor)
