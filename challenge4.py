#!/usr/bin/env python

import sys
import pyrax

if len(sys.argv) == 3:
    pyrax.set_credential_file("/home/graft/.rackspace_cloud_credentials")
    dns = pyrax.cloud_dns
    domain = [dom for dom in dns.list()
        if dom.name in sys.argv[1]][0]
    if not domain:
        name = raw_input("Enter a domain name: ")
        email = raw_input("Enter an e-mail address: ")
        domain = dns.create(name=name, emailAddress=email)
    record = {"type": "A", "name": sys.argv[1], "data":sys.argv[2], "ttl":1000}
    print domain.add_records(record)
else:
    print "Usage: %s domain.com 123.45.678.9" % sys.argv[0]

