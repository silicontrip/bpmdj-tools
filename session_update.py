#!/usr/local/bin/python2

import session_pb2
import sys
import json
import os.path

from pprint import pprint

def hextolong(h):
	ll = long(h,16)
	return -(ll & 0x8000000000000000) | (ll & 0x7fffffffffffffff)

def longtohex(l):
	return "%016x" % (l & 0xffffffffffffffff)


def catgid(segment):
	sid = ""
	sid += longtohex(segment.songGid1)
	sid += longtohex(segment.songGid2)
	sid += longtohex(segment.songGid3)
	sid += longtohex(segment.songGid4)

	return sid

def splitgid(gid):
	return [hextolong(gid[i:i+16]) for i in range(0, 64, 16)]

def findsid(db,name):

	fsid = None
	for k in db:
		pname = db[k]
		path,fname = os.path.split(pname)

		#print name, fname
		
		if fname == name:
			if fsid:
				print "duplicate find: " , k , pname
			else:
				print "found: " , k , pname
				fsid = k
		
	return fsid	



session = session_pb2.MixSessionProto()
sys.argv.pop(0) # remove arg0 aka calling program

with open(sys.argv.pop(0) , "r") as f: 
	db1 = json.loads(f.read())
	f.close()

with open(sys.argv.pop(0) , "r") as f: 
	db2 = json.loads(f.read())
	f.close()

with open(sys.argv.pop(0),"rb") as f:
	header = f.read(4)
	session.ParseFromString(f.read())
	f.close()

#print session 
# change data...

for sg in session.segments:
	sid = catgid(sg)
	if sid in db1:
		sname = db1[sid]
		path,name = os.path.split(sname)
		print name

		fid = findsid(db2,name)
		#print "Found: " , fid

		# leave unchanged if not found.
		if fid:
			songid = splitgid(fid)
			print "split: " , songid

			sg.songGid1 = songid[0]
			sg.songGid2 = songid[1]
			sg.songGid3 = songid[2]
			sg.songGid4 = songid[3]
		

with open(sys.argv.pop(0),"wb") as f:
	f.write(header);
	f.write(session.SerializeToString())
	f.close()
