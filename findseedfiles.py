# !/usr/bin/python3
import os
import sys
import oshash
import csv

#print ('Argument List:', str(sys.argv))
if (len(sys.argv) != 4 ) :
  sys.exit("You need to enter exactly 3 arguments:\n the scan list file,\n the source directory to scan (recursively),\n and the main directory to put the seeding folder(s) of symlinks")
  
listfile = sys.argv[1]
scandir = sys.argv[2]
newdir = sys.argv[3]

infile = open(listfile, "r")
read = csv.reader(infile,delimiter='|')
#headers = next(read) # skip header if needed
hashDict={}
    
#for each row
for row in read:
  hash = row[1]
  directory = row[0]
  # Add to dictionary 
  # note: will overwrite and store only single occurrence for each hash, no duplicates allowed
  hashDict[hash] = directory
        
# ok, now we scan for the files wanted
for root, dirs, files in os.walk(scandir, topdown = True):
    for name in files:
        fullpath = os.path.join(root, name)
        extension = os.path.splitext(fullpath)
        thehash = oshash.oshash(fullpath) + extension[1]
        if (thehash in hashDict):
           print ("File found to seed:",fullpath)
           os.makedirs( os.path.join(newdir, hashDict[thehash] ), exist_ok = True)
           newsymlink = os.path.join(newdir, hashDict[thehash], thehash)
           if (os.path.exists(newsymlink)):
              print ("file/symlink already exists:",newsymlink)
           else:
              os.symlink(fullpath, newsymlink)
