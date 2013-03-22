#!/usr/bin/env python
"""
<--Challenge 2-->
Write a script that clones a server (takes an image and deploys
the image as a new server).

@author: Neill Johnson
@date: March 15, 2013
"""

import os
import sys
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

# get a list of servers, and pick the first server in the list
server = cs.servers.list()
flavor = server[0].flavor['id']

# prompt user for input
img_name = raw_input("Input the image name: ")
serv_name = raw_input("Input the server name: ")

# image the first server
server[0].create_image(img_name)

# store the new image's info
clone_image = [img for img in cs.images.list()
        if img_name in img.name][0]

print "Waiting for image to finish building."
pyrax.utils.wait_until(clone_image, "status", ['ACTIVE', 'ERROR'], interval=20, attempts=40, verbose=True)


print "\nCreating server from image."
clone = cs.servers.create(serv_name, clone_image.id, flavor)
