import os.path
import json

class bpmdjdb:
	djdb = None

	def hextolong(self,h):
		ll = long(h,16)
		return -(ll & 0x8000000000000000) | (ll & 0x7fffffffffffffff)

	def longtohex(self,l):
		return "%016x" % (l & 0xffffffffffffffff)

	def catgid(self,segment):
		return  self.longtohex(segment.songGid1) + self.longtohex(segment.songGid2) + self.longtohex(segment.songGid3) + self.longtohex(segment.songGid4)  

	def splitgid(self,gid):
		return [self.hextolong(gid[i:i+16]) for i in range(0, 64, 16)]

	def readdb(self,fname):
		with open(fname , "r") as f: 
			self.djdb = json.loads(f.read())
			f.close()

	def gidsong(self,gid):
		if gid in self.djdb:
			return self.djdb[gid].encode('utf-8')

		return "NOT FOUND"

	def get (self,id):
		if id in self.djdb:
			return self.djdb[id]
		return None


	def findsid(self,name):

		fsid = None
		for k in self.djdb:
			pname = self.djdb[k]
			path,fname = os.path.split(pname)

		#print name, fname
		
			if fname == name:
				if fsid:
					print "duplicate find: " , k , pname
				else:
					print "found: " , k , pname
					fsid = k
		
		return fsid
