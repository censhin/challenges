#!/usr/bin/env python
"""
<--Challenge 6-->
Write a script that creates a CDN-enabled container in Cloud Files.

@author: Neill Johnson
@date: March 21, 2013
"""

import os
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

# prompt the user for input
cont_name = raw_input("Enter the name of your container: ")
cont_ttl = raw_input("Enter the ttl for your container in seconds(minimum 900): ")

# create a container and enable CDN
container = cf.create_container(cont_name)
container.make_public(ttl=cont_ttl)
cont = cf.get_container(container)

# print container information
print "<--Container Data-->"
print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri
