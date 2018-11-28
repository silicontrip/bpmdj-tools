#!/usr/local/bin/python2

import session_pb2
import sys
import json
import os.path

from bpmdjdb import bpmdjdb

from pprint import pprint

dj1 = bpmdjdb()
dj2 = bpmdjdb()

session = session_pb2.MixSessionProto()
sys.argv.pop(0) # remove arg0 aka calling program

dj1.readdb(sys.argv.pop(0))
dj2.readdb(sys.argv.pop(0))

with open(sys.argv.pop(0),"rb") as f:
	header = f.read(4)
	session.ParseFromString(f.read())
	f.close()

#print session 
# change data...

for sg in session.segments:
	sid = dj1.catgid(sg)
	sname = dj1.get(sid)
	if (sname):
		path,name = os.path.split(sname)
		print name

		fid = dj2.findsid(name)
		#print "Found: " , fid

		# leave unchanged if not found.
		if fid:
			songid = dj1.splitgid(fid)
			#print "split: " , songid

			sg.songGid1 = songid[0]
			sg.songGid2 = songid[1]
			sg.songGid3 = songid[2]
			sg.songGid4 = songid[3]
		

with open(sys.argv.pop(0),"wb") as f:
	f.write(header);
	f.write(session.SerializeToString())
	f.close()
