#!/usr/bin/env python
"""
<--Challenge 7-->
Write a script that will create 2 Cloud Servers and add them
as nodes to a new Cloud Load Balancer.

@author: Neill Johnson
@date: March 21, 2013
"""

import os
import time
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

# prompt for input, and store it for later use
lb_name = raw_input("Enter the load balancer's name: ")

srv1_name = raw_input("Enter the name for the first server: ")
srv1_img = raw_input("Enter which image you would like to use: ")
s1_img = [img for img in cs.images.list()
        if srv1_img in img.name][0]
srv1_ram = int(raw_input("Enter the amount of ram: "))
s1_ram = [flav for flav in cs.flavors.list()
        if srv1_ram == flav.ram][0]

srv2_name = raw_input("Enter the name for the second server: ")
srv2_img = raw_input("Enter which image you would like to use: ")
s2_img = [img for img in cs.images.list()
        if srv2_img in img.name][0]
srv2_ram = int(raw_input("Enter the amount of ram: "))
s2_ram = [flav for flav in cs.flavors.list()
        if srv2_ram == flav.ram][0]

# create servers
server1 = cs.servers.create(srv1_name, s1_img.id, s1_ram.id)
s1_id = server1.id
server2 = cs.servers.create(srv2_name, s2_img.id, s2_ram.id)
s2_id = server2.id

# wait for networking info to populate
while not (server1.networks and server2.networks):
    time.sleep(2)
    server1 = cs.servers.get(s1_id)
    server2 = cs.servers.get(s2_id)

# store server's private ip
s1_ip = server1.networks["private"][0]
s2_ip = server2.networks["private"][0]

# add servers as nodes
node1 = clb.Node(address=s1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=s2_ip, port=80, condition="ENABLED")

# create load balancer, and add nodes to it
vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(lb_name, port=80, protocol="HTTP",
        nodes=[node1, node2], virtual_ips=[vip])
