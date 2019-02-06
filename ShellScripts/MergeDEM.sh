#!/bin/bash
# curl -O [RAW]
# chmod u+x MergeDEM.sh
# place this file with your DEM files and run
ls -1 *.dem > dem_list.txt #  here we get all the .dem files only in a .txt index file
# below, not all flags are always needed, and there are many more.
# these specify 255 gradient, a file name, and that we are using an index file, not files one by one
gdal_merge.py -init "0 0 255" -o OUTPUT.tif --optfile dem_list.txt
# Hurrah
