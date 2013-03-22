#!/usr/bin/env python
"""
Challenge 3
@author: Neill Johnson
@date: March 16, 2013
"""

import os
import sys
import pyrax

"""
check to make sure there are two arguments
execute the script if there are
"""
if len(sys.argv) == 3:
    creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
    pyrax.set_credential_file(creds_file)
    cf = pyrax.cloudfiles

    """
    verify the directory we want to upload exists, then
    upload the contents of the folder and return the total bytes
    of the content along with the upload key
    """
    if os.path.exists(sys.argv[1]):
        upload_key, total_bytes = cf.upload_folder(sys.argv[1], container=sys.argv[2])
        current_bytes = cf.get_uploaded(upload_key)
        while current_bytes != total_bytes:
            current_bytes = cf.get_uploaded(upload_key)
            sys.stdout.write("%d bytes of %d bytes uploaded\r" % (current_bytes, total_bytes))
            sys.stdout.flush()
        print "%d bytes of %d bytes uploaded" % (current_bytes, total_bytes)
    else:
        print "Choose a valid directory to upload files from."
else:
    print "Usage: challenge3.py /path/to/file 'container name'"
