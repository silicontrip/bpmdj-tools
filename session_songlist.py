#!/usr/local/bin/python2

import session_pb2
import sys
import json
import binascii

def gidsong(gid):
	global djdb
	if sid in djdb:
		return djdb[gid].encode('utf-8')

	return "NOT FOUND"

def catgid(segment):
	sid = ""
	sid += "%016x" % (segment.songGid1  & 0xffffffffffffffff)
	sid += "%016x" % (segment.songGid2  & 0xffffffffffffffff)
	sid += "%016x" % (segment.songGid3  & 0xffffffffffffffff)
	sid += "%016x" % (segment.songGid4  & 0xffffffffffffffff)

	return sid



session = session_pb2.MixSessionProto()

sys.argv.pop(0)
with open(sys.argv.pop(0),"r") as f:
	djdb = json.loads(f.read())
	f.close()

for ag in sys.argv:
	print ag
	f=open(ag , "rb")
	try:
		f.seek(4)
		session.ParseFromString(f.read())
	except:
		continue
	f.close()

	print session.title.encode('utf-8')

	print "== SEGMENTS =="
	count=1
	for segment in session.segments:
		sid = catgid(segment)
		print count , sid , gidsong(sid)
		count += 1

	print 
	print "== CANDIDATES =="
	count = 1
	for candidate in session.candidates:
		sid = catgid(candidate)
		print count , sid , gidsong(sid)
		count += 1

	print 
	print "== CELLAR =="
	count = 1
	for cellar in session.cellar:
		sid = catgid (cellar.before)
		print count , sid , gidsong(sid)
		sid = catgid (cellar.after)
		print count , sid , gidsong(sid)
		count += 1

		 

	print ""
