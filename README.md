# GIS_Shortcuts

GDAL via Bash and Python 

...More is planned for this repo, a work in progress.  Cheers!

# Use GDAL to stitch DEM files pronto:

get these tools for mac using homebrew:

```
brew tap osgeo/osgeo4mac
brew install osgeo/osgeo4mac/qgis
# GDAL, Python, etc are all QGIS dependancies
# so just get all of them in one go
```

# In a terminal window:

```
cd Path/To/DEMData  # go to where the .dem files a re stored
ls -1 *.dem > dem_list.txt #  here we get all the .dem files only in a .txt index file 
# below, not all flags are always needed, and there are many more.
# these specify 255 gradient, a file name, and that we are using an index file, not files one by one 
gdal_merge.py -init "0 0 255" -o ../OUTPUT_FILENAME.tif --optfile dem_list.txt
# Hurrah
```
