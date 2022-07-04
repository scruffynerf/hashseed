# !/usr/bin/python3
import os
import sys
import oshash
import csv
import shutil

#print ('Argument List:', str(sys.argv))
if (len(sys.argv) < 3 ) :
  sys.exit("You need to enter 3 or 4 arguments:\n the scan list file,\n your seeding folder,\n and the main directory where we'll copy the newly downloaded items.\n FINALLY, if you put ALL as a 4th argument,\n then we will ALSO copy even the symlinked files (already in your collection) to the new location (and relink)")
  
listfile = sys.argv[1]
scandir = sys.argv[2]
newdir = sys.argv[3]

copyall = False
if (len(sys.argv) == 4):
   if (sys.argv[4] == "ALL"):
      copyall = True

infile = open(listfile, "r")
read = csv.reader(infile,delimiter='|')
#headers = next(read) # skip header if needed
hashDict={}

#for each row
for row in read:
  hash = row[1]
  directory = row[2]
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
           if (is_symlink(fullpath)) :
              print ("Symlink found, your collection should already have:",fullpath)
              if copyall:
                 print ("Copying file to new location as requested.")
                 newlocation = os.path.join(newdir, hashDict[thehash])
                 if (os.path.exists(newlocation)):
                    print ("File already exists:",newlocation)
                 else:
                    # make the path for everything but the filename itself
                    os.makedirs( os.path.dirname(newlocation), exist_ok = True)
                    # COPY the file to the new location
                    shutil.copy2(fullpath, newlocation)
                    # remove the old symlink for sanity, we'll only have one set of files linked
                    os.unlink(fullpath)
                    # symlink back so we can keep reseeding
                    os.symlink(newlocation, fullpath)                
           else:
              print ("File found to move (and relink):",fullpath)
              newlocation = os.path.join(newdir, hashDict[thehash])
              if (os.path.exists(newlocation)):
                 print ("File already exists:",newlocation)
              else:
                 # make the path for everything but the filename itself 
                 os.makedirs( os.path.dirname(newlocation), exist_ok = True)
                 # move the file to the new location
                 shutil.move(fullpath, newlocation)                  
                 # symlink back so we can keep reseeding
                 os.symlink(newlocation, fullpath)
