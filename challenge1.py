#!/usr/bin/env python

import pyrax
import time

def create_server(name="server", image="Ubuntu 12.04", flavor=512, num=1):
    """
    A method that accepts a string for a server name, a
    string for an image name, an integer for the amount of
    RAM for the server(s), and an integer to specify the
    number of servers to create, and returns a list of
    servers.
    """
    ubu_image = [img for img in cs.images.list()
        if image in img.name][0]
    flavor_512 = [flav for flav in cs.flavors.list()
        if flav.ram == flavor][0]
    server_list = []
    for i in range(1, num+1):
        server = cs.servers.create("%s%d"%(name, i), ubu_image.id, flavor_512.id)
        server_list.append(server)
    return server_list

def wait_for_server(server_list):
    for n in server_list:
        pyrax.utils.wait_until(n, "status", ['ACTIVE', 'ERROR'], interval=20, attempts=100, verbose=True)
    time.sleep(30)

def print_server_info(server_list):
    for n in server_list:
        print n
        if len(n.networks[u'public'][0]) <= 15:
            print "IP Address: %s" % n.networks[u'public'][0]
        else:
            print "IP Address: %s" % n.networks[u'public'][1]
        print "Password: %s" % n.adminPass

if __name__ == "__main__":
    pyrax.set_credential_file("/home/graft/.rackspace_cloud_credentials")
    cs = pyrax.cloudservers
    server_list = create_server(name="web", num=3)
    wait_for_server(server_list)
    print_server_info(server_list)
