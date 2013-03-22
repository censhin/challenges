#!/usr/bin/env python
"""
Challenge 4
@author: Neill Johnson
@date: March 16, 2013
"""

import os
import re
import sys
import pyrax


# verify we have 2 arguments, and execute the code if we do
if len(sys.argv) == 3:
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    dns = pyrax.cloud_dns

    # strip leading entries such as www. from FQDN
    name = re.split("^[^\.]+.", sys.argv[1])[1]

    # verify the domain exists, create it if it doesn't
    try:
        domain = [dom for dom in dns.list()
            if name in dom.name][0]
    except IndexError:
        print "DNS name: %s" % name
        email = raw_input("Enter an e-mail address: ")
        domain = dns.create(name=name, emailAddress=email)

    # create and add the record
    record = {"type": "A", "name": name, "data":sys.argv[2], "ttl":1000}
    print domain.add_records(record)
else:
    print "Usage: %s domain.com 123.45.678.9" % sys.argv[0]
