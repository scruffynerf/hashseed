#!/usr/bin/python3
import os
import sys
import oshash
import csv

#print ('Argument List:', str(sys.argv))
if (len(sys.argv) != 3 ) :
  sys.exit("You need to enter exactly 2 arguments: the source directory and the target directory")
  
scandir = sys.argv[1]
newdir = sys.argv[2]

with open(os.path.join(newdir,'list.csv'), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    for root, dirs, files in os.walk(scandir, topdown = True):
      for name in files:
        fullpath = os.path.join(root, name)
        if (os.path.getsize(fullpath) < 132000):
           continue
        extension = os.path.splitext(fullpath)
        thehash = oshash.oshash(fullpath) + extension[1]
        newsymlink = os.path.join(newdir, thehash)
        print (newdir,"|",thehash,"|",fullpath)
        writer.writerow([newdir, thehash, fullpath])
        if (os.path.exists(newsymlink)):
           print ("file/symlink already exists:",newsymlink)
        else:
           os.symlink(fullpath, newsymlink)
