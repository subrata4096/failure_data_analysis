#!/usr/bin/python
import sys
import os
from collections import *
#from Levenshtein import *
import hashlib

class libListFileInfo:
	liblistKey = ""
	username = ""
	jobid = 0
	def __init__(self, lkey, uname, jid):
		self.liblistKey = lkey
		self.username = uname
		self.jobid = jid
	

def doClustering(mylist, threshold):
	clusters = defaultdict(list)
	numb = range(len(mylist))
	for i in numb:
        	for j in range(i+1, len(numb)):
			if distance(mylist[i].liblistKey,mylist[j].liblistKey) <= threshold:
				#print mylist[j].liblistKey
                		clusters[i].append(mylist[j].liblistKey)
                		clusters[j].append(mylist[i].liblistKey)
	return clusters

def getLibKey(fileName):
	 with open(fileName, 'r') as infile:
	 	lines = []
	 	for line in infile:
	 		line = line.strip()
			#print line
			if (line == ""):
				continue
			lines.append(line)
	 #sort the library list to normalize. this is to take care of address space randomization
	 lines.sort()
      	 libkey = ','.join(lines)
	 #print libkey
	 hash_object = hashlib.md5(libkey.encode())
	 hashkey = hash_object.hexdigest()
	 hashkeyStr = str(hashkey)
	 return hashkey
	 
         
def makeLibListKey(fileName):
	baseFileName = os.path.basename(fileName)
	#print baseFileName
	try:
		user_jobid = baseFileName.split('.')[0]
		fields = user_jobid.split('_')
		userName = fields[0]
		jobid = int(fields[1])
        #print userName, jobid

		libraryKey = getLibKey(fileName)
		libinfo = libListFileInfo(libraryKey, userName, jobid)
		return libraryKey, libinfo
	except:
		return "",None
 	
def getAllFiles(dirName):
	libraryList = []
	for root, dirnames, filenames in os.walk(dirName):
		for filename in filenames:
			f = (os.path.join(root, filename))
			baseFileName = os.path.basename(f)
			if(baseFileName.find("liblist") == -1):
				continue
			#print f
			libraryKey, libinfo = makeLibListKey(f)
			if(libraryKey == ""):
				continue
			libraryList.append(libinfo)
	return libraryList

def identify_similar_jobs(libList):
	jobMap = {}
	for l in libList:
        	lkey = l.liblistKey
		if lkey in jobMap.keys():
			jobMap[lkey].append(l.jobid)
		else:	
			jobMap[lkey] = []
			jobMap[lkey].append(l.jobid)
	return jobMap
if __name__ == "__main__":
	dName = sys.argv[1]
	#print dName
	libList = getAllFiles(dName)
        #for l in libList:
		#print l.liblistKey

        #clusters = doClustering(libList,0)	
	#print clusteris
	jMap = identify_similar_jobs(libList)
	#print jMap
	print "\n Identifying same jobids\n"
	with open("grouped_jobs.txt", 'w') as outfile:
		outfile.write("========= same jobs ==========\n")
		for k in jMap.keys():
			jobstr= ""
			for j in jMap[k]:
				jobstr += str(j) + ", "
			outfile.write(jobstr)
			outfile.write("\n----------- next set ------------------\n")
		outfile.flush()
