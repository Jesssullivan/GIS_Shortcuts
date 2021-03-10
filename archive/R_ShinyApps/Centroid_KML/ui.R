ui <- fluidPage(
  titlePanel("Centroid KML Generator"),
  sidebarLayout(
    mainPanel(
      fileInput("file", "Choose Your Input KML File"),
      print("This input file must contain waypoints or point data!"),
      width = 12
    ),
    sidebarPanel(
      actionButton("go", "Click to Run..."),
      downloadButton("downloadcent", "Click to download your new centroid as a KML point!"),
      width = 6)
  )
)
