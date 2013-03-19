#!/usr/bin/env python

import os
import re
import sys
import pyrax

if len(sys.argv) == 3:
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    dns = pyrax.cloud_dns
    name = re.split("^[^\.]+.", sys.argv[1])[1]
    try:
        domain = [dom for dom in dns.list()
            if name in dom.name][0]
    except IndexError:
        print "DNS name: %s" % name
        email = raw_input("Enter an e-mail address: ")
        domain = dns.create(name=name, emailAddress=email)
    record = {"type": "A", "name": name, "data":sys.argv[2], "ttl":1000}
    print domain.add_records(record)
else:
    print "Usage: %s domain.com 123.45.678.9" % sys.argv[0]
