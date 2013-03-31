#!/usr/bin/env python
"""
<--Challenge 10-->
Write an application that will:
    1) Create 2 servers, supplying a ssh key to be
       installed at /root/.ssh/authorized_keys.
    2) Create a load balancer
    3) Add the 2 new servers to the LB
    4) Set up LB monitor and custom error page.
    5) Create a DNS record based on a FQDN for the
       LB VIP.
    6) Write the error page html to a file in cloud
       files for backup

@author: Neill Johnson
@date: March 30, 2013
"""

import os
import re
import sys
import time
import pyrax

def create_server(name, ssh_key):
    cs = pyrax.cloudservers
    files = {"/root/.ssh/authorized_keys": ssh_key}
    image = [img for img in cs.images.list()
            if "Ubuntu 12.04" in img.name][0]
    flavor = [flav for flav in cs.flavors.list()
            if flav.ram == 512][0]
    server = cs.servers.create(name, image.id, flavor.id, files=files)
    return server

def create_chal10_servers():
    cs = pyrax.cloudservers
    serv_name = raw_input("Name your servers: ")
    ssh_key = raw_input("Path to ssh key: ")
    print
    servers = []
    for i in range(2):
        name = "%s%s" % (serv_name, (i+1))
        print "Creating %s..." % name
        servers.append(create_server(name, ssh_key))
        time.sleep(5)
    print
    for n in servers:
        print "server: %s, password: %s" % (n.name, n.adminPass)
        while not n.networks:
            if n.status == "ERROR":
                print "Error creating %s" % n.name
                exit(-1)
            time.sleep(3)
            n = cs.servers.get(n.id)
    print
    return servers

def create_lb(servers):
    cs = pyrax.cloudservers
    clb = pyrax.cloud_loadbalancers
    name = raw_input("Name your load balancer: ")
    nodes = []
    for i in range(len(servers)):
        serv = servers[i]
        server = cs.servers.get(serv.id)
        addr = server.networks["private"][0]
        nodes.append(clb.Node(address=addr, port=80, condition="ENABLED"))
    vip = clb.VirtualIP(type="PUBLIC")
    print "Creating %s..." % name
    lb = clb.create(name, port=80, protocol="HTTP", nodes=nodes, virtual_ips=[vip])
    print
    return lb

def html_upload(content):
    cf = pyrax.cloudfiles
    cont = cf.list_containers()
    while True:
        print cont
        pick = raw_input("Pick a container: ")
        if pick in cont:
            obj = cf.store_object(pick, "error_page.html", content)
            print "Stored object: ", obj
            break
        else:
            print "Pick a different container."

def create_chal10_lb(servers):
    clb = pyrax.cloud_loadbalancers
    lb = create_lb(servers)
    pyrax.utils.wait_until(lb, "status", ["ACTIVE", "ERROR"], interval=20,
            attempts=40, verbose=True)
    print "\nCreating LB monitor..."
    lb.add_health_monitor(type="CONNECT", delay=10, timeout=10,
            attemptsBeforeDeactivation=3)
    print "Creating LB error page..."
    pyrax.utils.wait_until(lb, "status", ["ACTIVE", "ERROR"], interval=20,
            attempts=40, verbose=True)
    html = "<html><body>Challenge10 Error Page</body></html>"
    html_upload(html)
    clb.set_error_page(lb.id, html)
    return lb

def test_fqdn(fqdn):
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

def create_dns(lb_vip):
    dns = pyrax.cloud_dns
    print "Creating domain..."
    dom_name = raw_input("Enter a domain name: ")
    email = raw_input("Enter an e-mail address for your domain: ")
    chk_fqdn, dom_name = test_fqdn(dom_name)
    domain = dns.create(name=dom_name, emailAddress=email)
    print "A Record"
    record = {"type": "A", "name": dom_name, "data": lb_vip, "ttl": 1200}
    print domain.add_records(record)
    print "CNAME Record"
    record = {"type": "CNAME", "name": chk_fqdn, "data": dom_name, "ttl": 1200}
    print domain.add_records(record)

def main():
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    servers = create_chal10_servers()
    lb = create_chal10_lb(servers)
    lb_vip = lb.virtual_ips[0].address
    dns = create_dns(lb_vip)

if __name__ == "__main__":
    main()
