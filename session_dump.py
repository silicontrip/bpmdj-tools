#!/usr/local/bin/python2

import session_pb2
import sys
import json

from pprint import pprint

from bpmdjdb import bpmdjdb

djdb = bpmdjdb()

session = session_pb2.MixSessionProto()
sys.argv.pop(0) # remove arg0 aka calling program

with open(sys.argv.pop(0),"rb") as f:
	header = f.read(4)
	print "header: " + header 
	session.ParseFromString(f.read())
	f.close()

for sg in session.segments:
	id = djdb.catgid(sg)
	print id
	ll = djdb.splitgid(id)
	print id, ll

print

print session 
