import os.path
class bpmdjdb:
	djdb = None

def hextolong(h):
	ll = long(h,16)
	return -(ll & 0x8000000000000000) | (ll & 0x7fffffffffffffff)

def longtohex(l):
	return "%016x" % (l & 0xffffffffffffffff)

def catgid(segment):
	return [ longtohex(segment.songGid1) + longtohex(segment.songGid2) + longtohex(segment.songGid3) + longtohex(segment.songGid4)  ]

def splitgid(gid):
	return [hextolong(gid[i:i+16]) for i in range(0, 64, 16)]

def readdb(fname):
	with open(fname , "r") as f: 
		self.djdb = json.loads(f.read())
		f.close()

def findsid(name):

	fsid = None
	for k in self.djdb:
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
