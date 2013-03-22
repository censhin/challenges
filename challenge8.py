#!/usr/bin/env python
"""
<--Challenge 8-->
Write a script that will create a static webpage served out of
Cloud Files. The script must create a new container, cdn enable
it, enable it to serve an index file, create an index file
object, upload the object to the container, and create a CNAME
record pointing to the CDN URL of the container.

@author: Neill Johnson
@date: March 21, 2013
"""

import os
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns

# name the html file, and define its contents
page = "index.html"
contents = "<!DOCTYPE html>\n<html>\n<body>\n\n<h1>"
contents = contents + "Challenge 8</h1>\n\n</body>\n</html>"

"""
create the container to hold the html file
and enable CDN
"""
container = cf.create_container("index")
container.make_public(ttl=1200)
cont = cf.get_container(container)

# create the file and store it
obj = cont.store_object(page, contents)
print "Stored object:", obj

# set the file to be the container's index page
cont.set_web_index_page(page)
print "Set %s to container index page." % page

# prompt for user input, and create a DNS instance
name = raw_input("Enter your DNS domain name: ")
email = raw_input("Enter your DNS e-mail: ")
domain = dns.create(name=name, emailAddress=email)

"""
create a CNAME record for the DNS instance, and
point it to the CDN URI of the container
"""
name = "cdn." + name
record = {"type": "CNAME", "name": name, "data": cont.cdn_uri, "ttl":1000}
domain.add_records(record)
