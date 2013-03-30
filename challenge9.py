#!/usr/bin/env python
"""
<--Challenge 9-->
Write an application that when passed the arguments FQDN, image,
and flavor it creates a server of the specified image and flavor
with the same name as the fqdn, and creates a DNS entry for the
fqdn pointing to the server's public IP.

@author: Neill Johnson
@date: March 29, 2013
"""

import os
import re
import sys
import pyrax

def test_fqdn(fqdn):
    """
    Test that our FQDN is correct, and return the FQDN and the
    domain name.
    """
    prefix = fqdn.split(".")[0]
    dom_name = re.split("^[^\.]+.", fqdn)[1]
    while True:
        answer = raw_input("Is your FQDN \"%s\" correct? (y/n): " % fqdn)
        answer.lower()
        if answer == "y":
            fqdn = (prefix + "." + dom_name)
            return (fqdn, dom_name)
        elif answer == "n":
            fqdn = raw_input("Enter the correct FQDN: ")
            prefix = fqdn.split(".")[0]
            dom_name = re.split("^[^\.]+.", fqdn)[1]
        else:
            print "Enter y or n."


def create_server(name=sys.argv[1], image=sys.argv[2], flavor=sys.argv[3]):
    """
    Create a server with our command line arguments, and return
    that server's public IP address.
    """
    cs = pyrax.cloudservers
    img = [img for img in cs.images.list() if image in img.name][0]
    flav = [flav for flav in cs.flavors.list() if int(flavor) == flav.ram][0]
    server = cs.servers.create(name, img.id, flav.id)
    print "Creating server."
    pyrax.utils.wait_until(server, "status", ["ACTIVE", "ERROR"], interval=20, attempts=40, verbose=True)
    print
    serv_data = cs.servers.get(server.id)
    server_ip = serv_data.networks["private"][0]
    return server_ip

def create_domain(server_ip, fqdn=sys.argv[1]):
    """
    Create a Cloud DNS domain with an A record pointing to the
    IP address of a server, and a CNAME record for the FQDN.
    """
    dns = pyrax.cloud_dns
    chk_fqdn, dom_name = test_fqdn(fqdn)
    print "Creating domain."
    email = raw_input("Enter an e-mail address for your domain: ")
    domain = dns.create(name=dom_name, emailAddress=email)
    print "A Record"
    record = {"type": "A", "name": dom_name, "data": server_ip, "ttl": 1200}
    print domain.add_records(record)
    print "CNAME Record"
    record = {"type": "CNAME", "name": chk_fqdn, "data": dom_name, "ttl": 1200}
    print domain.add_records(record)

def main():
    """
    The main function. Executes the code to create a server and
    a DNS entry for that server with an A record pointing to
    the server's IP address and a CNAME record pointing to the
    FQDN.
    """
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    server_ip = create_server()
    create_domain(server_ip)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        main()
    else:
        print "Usage: %s www.example.com server_image(eg. Ubuntu 12.04) ram(eg. 512)" % sys.argv[0]
