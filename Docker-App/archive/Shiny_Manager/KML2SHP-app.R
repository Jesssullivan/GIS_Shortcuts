# KML2SHP-app.R
# single page app for dist
#
library(shiny)
library(rgdal)
library(gdalUtils)
args <- commandArgs(trailingOnly = TRUE)

ui <- fluidPage(
  titlePanel(
    "KML to SHP Converter"),
  sidebarLayout(
    mainPanel(
      fileInput("file", "Choose Your Input KML File", multiple = TRUE),
      width = 12
    ),
    sidebarPanel(
      actionButton("go", "Click to Run..."),
      downloadButton("downloadcent", "Click to Download a .zip of the resulting SHP files.
                     If not all are converted, please verify your KML layers!"),
      width = 12)
  )
)

server <- function(input, output) {
  observeEvent(input$go, {
    dat <- input$file
    out <- input$outfile
    datum <- dat$datapath
    tempfile <- "shp"
    ogr2ogr(datum, tempfile, overwrite = TRUE)
    zip(zipfile='zip', files=tempfile)
    output$downloadcent <- downloadHandler(filename = function() {
      paste("kml2shp-", Sys.Date(), ".zip", sep="")
    },
    content = function(con) {
      file.copy('zip.zip', con)
    })
  })
}

runApp(shinyApp(ui, server), port = as.numeric(args[1]))
