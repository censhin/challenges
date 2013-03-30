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
    servers = []
    for i in range(2):
        name = "%s%s" % (serv_name, (i+1))
        print "Creating %s" % name
        servers.append(create_server(name, ssh_key))
        time.sleep(5)
    for n in servers:
        print "server: %s, password: %s" % (n.name, n.adminPass)
        while not n.networks:
            if n.status == "ERROR":
                print "Error creating %s" % n.name
                exit(-1)
            time.sleep(3)
            n = cs.servers.get(n.id)
    return servers

def create_lb(servers):
    clb = pyrax.cloud_loadbalancers
    name = raw_input("Name your load balancer: ")
    nodes = []
    for i in len(servers):
        addr = servers[i].networks["private"][0]
        nodes.append(clb.Node(address=addr, port=80, condition="ENABLED"))
    vip = clb.VirtualIP(type="PUBLIC")
    lb = clb.create(name, port=80, protocol="HTTP", nodes=nodes, virtual_ips=[vip])
    return lb

def create_chal10_lb(servers):
    lb = create_lb(servers)
    lb.add_health_monitor(type="CONNECT", delay=10, timeout=10,
            attemptsBeforeDeactivation=3)
    ep_mgr = lb.errorpage()
    html = "<html><body>Challenge10 Error Page</body></html>"
    ep_mgr.add(html)
    return lb

def create_dns():
    pass
    #dns = pyrax.cloud_dns

def main():
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    servers = create_chal10_servers()
    lb = create_chal10_lb(servers)
    print lb.virtual_ips[0].address

if __name__ == "__main__":
    main()
