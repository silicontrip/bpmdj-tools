#!/usr/local/bin/python2

import session_pb2
import sys
import json

from pprint import pprint

def longtohex(l):
	return "%016x" % (l & 0xffffffffffffffff)

def hextolong(h):
	ll = long(h,16)
	return -(ll & 0x8000000000000000) | (ll & 0x7fffffffffffffff)

def catgid(segment):
	sid = ""
	sid += longtohex(segment.songGid1)
	sid += longtohex(segment.songGid2)
	sid += longtohex(segment.songGid3)
	sid += longtohex(segment.songGid4)

	return sid

def splitgid(gid):
	sa  = [gid[i:i+16] for i in range(0, 64, 16)]
#	print sa
	la = []
	for id in sa:
		ll = hextolong(id)
#		print id, ll
		la.append(ll)

	return la



session = session_pb2.MixSessionProto()
sys.argv.pop(0) # remove arg0 aka calling program
#f=open(sys.argv.pop(0) , "r")
#djdb = json.loads(f.read())
#f.close()

with open(sys.argv.pop(0),"rb") as f:
	header = f.read(4)
	print "header: " + header 
	session.ParseFromString(f.read())
	f.close()

for sg in session.segments:
	id = catgid(sg)
	ll = splitgid(id)
	print id, ll

print

print session 
