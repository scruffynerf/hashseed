# hashseed

This software uses OSHash to:

- generate a list of a set of files
- scan a directory for matches to that set of files and symlink them per the list
- handle additional files added later that aren't symlinks but that are on the list

Usage:

`python3 makelist.py`
You need to enter exactly 2 arguments: the source directory and the target directory

`python3 findseedfiles.py`
You need to enter exactly 3 arguments:
- the scan list file,
- the source directory to scan (recursively),
- and the main directory to put the seeding folder(s) of symlinks

`python3 renamefinished.py`
You need to enter 3 or 4 arguments:
- the scan list file,
- your seeding folder,
- and the main directory where we'll copy the newly downloaded items.
- FINALLY, if you put ALL as a 4th argument,
-- then we will ALSO copy even the symlinked files (already in your collection) to the new location (and relink)
