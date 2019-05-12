## LiDAR derived Raster --> STL conversion ##
#
# By Jess Sullivan
#
# This is a generic implimentation of the r2stl library, and is returning
# 3d form to DEM data by pixel value (z value) as an STL.  
#

# Libraries
library(r2stl) # XYZ conversion
library(magick) # basic image processing and conversion

# PNG Conversion- R image processing is easier with greyscale PNG.

image = image_read("../Raster_Domain-tif/Rast6.tif")
imag <- image_convert(image, format = "png", colorspace = "gray")
ima <- image_write(imag, "converted.png")
im <- load.image("converted.png")

# define 3d matrix from pixel value
z <- im[ , , 1, 1]
x <- 1:length(im[, 1, 1, 1])
y <- 1:length(im[1, , , 1])

# convert
r2stl(x, y, z, filename = "R_STL-Output.stl", object.name = "R_STL-Output", show.persp = TRUE)

