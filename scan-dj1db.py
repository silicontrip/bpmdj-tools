#!/usr/bin/python

import os
import fnmatch
import sys
import binascii
import json

djdb={}
for root, dir, files in os.walk(sys.argv[1]):
        for items in fnmatch.filter(files, "*.bpmdj1"):
                djfn =  root + os.sep +  items
                try:
                        f = open(djfn, "rb")
                        f.seek(4)
                        sid = ""
                        for id in range(4):
                                byte = f.read(8)
                                sid += binascii.hexlify(byte)

                        djdb[sid] = djfn
                finally:
                    f.close()


print json.dumps(djdb,indent=4)
