library(shiny)
library(rgdal)
library(sf)
library(geosphere)
library(plyr)
library(tidyverse)

server <- function(input, output) {
  observeEvent(input$go, {
    dat <- input$file
    datum <- dat$datapath
    kml_cleaned <- ogrListLayers(datum)
    it <- as.numeric(length(kml_cleaned)) 
    iterate_layers <- function(i){
      layer_i <- st_read(datum, kml_cleaned[i])
      print(layer_i)
      return(layer_i)
    }
    rate <- 1:it
    data <- data.frame(t(data.frame(sapply(rate, iterate_layers))))
    # extract centroid with WGS84 CRS
    lengthdata <- as.numeric(length(data))
    # pull lat/lon function
    func <- function(i) {
      lm <- as.numeric(length(unlist(data$geometry)))
      getGeo <- array(unlist(data$geometry), dim = c(3,lm))
      getGeo <- array(unlist(getGeo), dim=c(lm, 3))
      coords <- cbind(getGeo[1], getGeo[2])
      return(coords)
    }
    # generate centroid with geosphere function from table of coords
    df <- data.frame(matrix(nrow = 1, ncol = 2))
    cent_in <- as.matrix(t(sapply(2, func)))
    cent_sp <- SpatialPointsDataFrame(cent_in, df, proj4string=CRS("+proj=longlat +datum=WGS84"))
    # write out lat long as a new kml file
    target_file <- "KML_Centroid.kml"
    results <- writeOGR(cent_sp, dsn = target_file, layer = "", driver="KML")
    output$downloadcent <- downloadHandler(filename = function() {
      paste("Centroid-", Sys.Date(), ".kml", sep="")
    },
    content = function(con) {
      file.copy(target_file, con)
    })
  })
}






