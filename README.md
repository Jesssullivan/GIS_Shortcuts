# GIS Shortcuts

<img title='3d From the command line....' src="Python_Results.png" width='500px' >

* * *  

*Miscellaneous gis notes, mostly derived from [my blog over here](https://www.transscendsurvival.org/)*

* * *  

**Index:**  <br>

[**GDAL Shell macros from R**](#rmacros) <br>
[**GDAL setup on Mac OSX**](#osx) <br>
[**Ubuntu GDAL setup on Windows WSL**](#wsl) <br>
[**GDAL from Bash- DEM stitching**](#demstitch) <br>


* * *


***Some GDAL shell macros from R instead of rgdal***  

[Visit this blog post](https://www.transscendsurvival.org/2020/03/01/1607/)

*it's not R sacrilege if nobody knows*    

<h4 id="rmacros"> </h4>     

Even the little stuff benefits from some organizational scripting, even if it’s just to catalog one’s actions.  Here are some examples for common tasks.


Get all the source data into a R-friendly format like csv.  `ogr2ogr` has a nifty option `-lco GEOMETRY=AS_WKT` (Well-Known-Text) to keep track of spatial data throughout abstractions- we can add the WKT as a cell until it is time to write the data out again.   
```
# define a shapefile conversion to csv from system's shell:
sys_SHP2CSV <- function(shp) {
  csvfile <- paste0(shp, '.csv')
  shpfile <-paste0(shp, '.shp')
  if (!file.exists(csvfile)) {
    # use -lco GEOMETRY to maintain location
    # for reference, shp --> geojson would look like:
    # system('ogr2ogr -f geojson output.geojson input.shp')
    # keeps geometry as WKT:
    cmd <- paste('ogr2ogr -f CSV', csvfile, shpfile, '-lco GEOMETRY=AS_WKT')
    system(cmd)  # executes command
  } else {
    print(paste('output file already exists, please delete', csvfile, 'before converting again'))
  }
  return(csvfile)
}
```

Read the new csv into R:
```
# for file 'foo.shp':
foo_raw <- read.csv(sys_SHP2CSV(shp='foo'), sep = ',')
```

One might do any number of things now, some here lets snag some columns and rename them:
```
# rename the subset of data "foo" we want in a data.frame:
foo <- data.frame(foo_raw[1:5])
colnames(foo) <- c('bar', 'eggs', 'ham', 'hello', 'world')
```

We could do some more careful parsing too, here a semicolon in cell strings can be converted to a comma:
```
# replace ` ; ` to ` , ` in col "bar":
foo$bar <- gsub(pattern=";", replacement=",", foo$bar)
```

Do whatever you do for an output directory:
```
# make a output file directory if you're into that
# my preference is to only keep one set of output files per run
# here, we'd reset the directory before adding any new output files
redir <- function(outdir) {
  if (dir.exists(outdir)) {
    system(paste('rm -rf', outdir))
  }
  dir.create(outdir)
}
```

Even though this is totally adding a level of complexity to what could be a single `ogr2ogr`  command, I've decided it is still worth it- I'd definitely rather keep track of everything I do over forget what I did.... xD

```
# make some methods to write out various kinds of files via gdal:
to_geoJSON <- function(target) {
  print(paste('converting', target, 'to geojson .... '))
  system(paste('ogr2ogr -f', " geojson ",  paste0(target, '.geojson'), paste0(target, '.csv')))
}

to_SHP <- function(target) {
  print(paste('converting ', target, ' to ESRI Shapefile .... '))
  system(paste('ogr2ogr -f', " 'ESRI Shapefile' ",  paste0(target, '.shp'), paste0(target, '.csv')))
}

# name files:
foo_name <- 'output_foo'

# for table data 'foo', first:
write.csv(foo, paste0(foo_name, '.csv'))

# convert with the above csv:
to_geoJSON(foo_name)
to_SHP(foo_name)
```

* * *

**Using GDAL on Mac OSX**

<h4 id="osx"> </h4>     

[Visit this blog post](https://www.transscendsurvival.org/2019/10/07/gdal-for-gis-on-unix-using-a-mac-or-better-linux/)

Note: in my opinion, homebrew and macPorts are good ideas- try them!  If you don’t have it, get it now:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
(….However, port or brew installing QGIS and GDAL (primarily surrounding the delicate links between QGIS / GDAL / Python 2 & 3 / OSX local paths) can cause baffling issues.  If possible, don’t do that.  Use QGIS installers from the official site and build from source!)

if you need to resolve issues with your GDAL packages via removal:
on MacPorts, try similar:
```
sudo port uninstall qgis py37-gdal

# on homebrew, list then remove (follow its instructions):

brew list
brew uninstall gdal geos gdal2  
```     
*!!! NOTE: I am investigating more reliable built-from-source solutions for gdal on mac.*      

Really!

There are numerous issues with brew-installed gdal.  Those I have run into include:
- linking issues with the crucial directory “gdal-data” (libraries)
- linking issues Python bindings and python 2 vs. 3 getting confused
- internal raster library conflicts against the gdal requirements
- Proj.4 inconsistencies (see source notes below)
- OSX Framework conflicts with source / brew / port (http://www.kyngchaos.com/software/frameworks/)
- Linking conflicts with old, qgis default / LTR libraries against new ones
- Major KML discrepancies: expat standard vs libkml.  
```
brew install gdal
#
# brew install qgis can work well too.  At least you can unbrew it!
#
```

Next, assuming your GDAL is not broken (on Mac OS this is rare and considered a miracle):

```
# double check CLI is working:
gdalinfo --version
# “GDAL 2.4.0, released 2018/12/14”
gdal_merge.py
# list of args
```

<h4 id="wsl"> </h4>     

**Using Ubuntu GDAL on Windows w/ WSL**

[LINK: get the WSL shell from Microsoft](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

```
# In the WSL shell:

sudo apt-get install python3.6-dev -y
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install libgdal-dev -y
sudo apt-get install gdal-bin -y

# See here for more notes including Python bindings:
# https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html
```     

***In a new Shell:***

```
# Double check the shell does indeed have GDAL in $PATH:
gdalinfo --version

```

*To begin- try a recent GIS assignment that would otherwise rely on the ESRI mosaic system:*

<h4 id="demstitch"> </h4>     

Data source: ftp://ftp.granit.sr.unh.edu/pub/GRANIT_Data/Vector_Data/Elevation_and_Derived_Products/d-elevationdem/d-10m/

!!  Warning!  These files are not projected in a way ESRI or GDAL understands.  They WILL NOT HAVE A LOCATION IN QGIS.  They will, however, satisfy the needs of the assignment.     

```
# wget on mac is great.  This tool (default on linux) lets us grab GIS data from
# most providers, via FTP and similar protocols.

brew install wget
```
make some folders
```
mkdir GIS_Projects && cd GIS_Projects
```
use wget to download every .dem file (-A .dem) from the specified folder and sub-folders (-r)
```
wget -r -A .dem ftp://ftp.granit.sr.unh.edu/pub/GRANIT_Data/Vector_Data/Elevation_and_Derived_Products/d-elevationdem/

cd ftp.granit.sr.unh.edu/pub/GRANIT_Data/Vector_Data/Elevation_and_Derived_Products/d-elevationdem
```
make an index file of only .dem files.  
(If we needed to download other files and keep them from our wget (more common)
this way we can still sort the various files for .dem)
```
ls -1 *.dem > dem_list.txt
```
use gdal to make state-plane referenced “Output_merged.tif” from the list of files
in the index we made.
it will use a single generic "0 0 255" band to show gradient.  

```
gdal_merge.py -init "0 0 255" -o Output_Merged.tif --optfile dem_list.txt
```
copy the resulting file to desktop, then return home
```
cp Output_Merged.tif ~/desktop && cd
```
if you want (recommended):
```
rm -rf GIS_Projects  # remove .dem files.  Some are huge!
```
In Finder at in ~/desktop, open the new file with QGIS.  A normal photo viewer will NOT show any detail.  

Need to make something like this a reusable script?  In Terminal, just a few extra steps:
```
mkdir GIS_Scripts && cd GIS_Scripts
```
open an editor + filename.  Nano is generally pre-installed on OSX.
```
nano GDAL_LiveMerge.sh
```
COPY + PASTE THE SCRIPT FROM ABOVE INTO THE WINDOW
 - ctrl+X , then Y for yes

make your file runnable:
```
chmod u+x GDAL_LiveMerge.sh
```
run with ./
```
./GDAL_LiveMerge.sh
```     

You can now copy + paste your script anywhere you want and run it there.  scripts like this should not be exported to your global path / bashrc and will only work if they are in the directory you are calling them:  If you need a global script, there are plenty of ways to do that too.

*See /Notes_GDAL/README.md for notes on building GDAL from source on OSX*

<img title='Results' src="GDAL_Bash_DEM_Merge.png" width='300px' >  

# xD
