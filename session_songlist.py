#!/usr/local/bin/python2

import session_pb2
import sys
import json
import binascii

from bpmdjdb import bpmdjdb

session = session_pb2.MixSessionProto()

sys.argv.pop(0)

djdb = bpmdjdb()
djdb.readdb(sys.argv.pop(0))

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
		sid = djdb.catgid(segment)
		print count , sid , djdb.gidsong(sid)
		count += 1

	print 
	print "== CANDIDATES =="
	count = 1
	for candidate in session.candidates:
		sid = djdb.catgid(candidate)
		print count , sid , djdb.gidsong(sid)
		count += 1

	print 
	print "== CELLAR =="
	count = 1
	for cellar in session.cellar:
		sid = djdb.catgid (cellar.before)
		print count , sid , djdb.gidsong(sid)
		sid = djdb.catgid (cellar.after)
		print count , sid , djdb.gidsong(sid)
		count += 1

	print ""
