#!/usr/bin/env python
"""
<--Challenge 4-->
Write a script that uses Cloud DNS to create a new A record when
passed a FQDN and IP address as arguments.

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

    # ensure the FQDN is correct
    prefix = sys.argv[1].split(".")[0]
    name = re.split("^[^\.]+.", sys.argv[1])[1]
    if prefix != "www":
        print "Warning: domain not prefixed with www."
        while True:
            answer = raw_input("Did you mean \"%s\" to be your prefix? (y/n): " % prefix)
            answer.lower()
            if answer == "y":
                break
            elif answer == "n":
                prefix = raw_input("Enter your FQDN prefix: ")
            else:
                print "Enter y or n."

    while True:
        answer = raw_input("Is your FQDN \"%s\" correct? (y/n): " % (prefix + "." + name))
        answer.lower()
        if answer == "y":
            fqdn = (prefix + "." + name)
            break
        elif answer == "n":
            fqdn = raw_input("Enter the correct FQDN: ")
            prefix = re.split("^[^\.]+.", fqdn)[0]
            name = re.split("^[^\.]+.", fqdn)[1]
        else:
            print "Enter y or n."

    # verify the domain exists, create it if it doesn't
    try:
        domain = [dom for dom in dns.list()
            if name in dom.name][0]
    except IndexError:
        print "DNS name: %s" % name
        email = raw_input("Enter an e-mail address: ")
        print "Creating domain."
        domain = dns.create(name=name, emailAddress=email)

    # create and add the record
    print "A Record"
    record = {"type": "A", "name": name, "data": sys.argv[2], "ttl":1000}
    print domain.add_records(record)
    print "CNAME Record for FQDN"
    record = {"type": "CNAME", "name": fqdn, "data": name, "ttl":1000}
    print domain.add_records(record)
else:
    print "Usage: %s www.domain.com 123.45.678.9" % sys.argv[0]
    print "FQDN should be prefixed"
    print "eg. www.domain.com or admin.domain.com"
