#!/usr/bin/env python

import os
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns
page = "index.html"
contents = "<!DOCTYPE html>\n<html>\n<body>\n\n<h1>"
contents = contents + "Challenge 8</h1>\n\n</body>\n</html>"

container = cf.create_container("index")
container.make_public(ttl=1200)
cont = cf.get_container(container)

obj = cont.store_object(page, contents)
print "Stored object:", obj

cont.set_web_index_page(page)
print "Set %s to container index page." % page

name = raw_input("Enter your DNS domain name: ")
email = raw_input("Enter your DNS e-mail: ")
domain = dns.create(name=name, emailAddress=email)
name = "cdn." + name
record = {"type": "CNAME", "name": name, "data": cont.cdn_uri, "ttl":1000}
domain.add_records(record)
