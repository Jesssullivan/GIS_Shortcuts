library(shiny)

setwd('/Users/jesssullivan/git/Shiny-Apps/Docker-App/shiny')

baseport <- 3111
maxport <- 8111
max_elap <- -300 # secs
# init port df 
numports <- 0
ActivePorts <- data.frame(c('','',''))


ui <- fluidPage(
  
  titlePanel(
    "Shiny App Manager"),
  mainPanel(
    actionButton('default', 'Start Default Shiny Geyser App'),
    actionButton('KML2SHP', 'Run KML2SHP App!'),
    # actionButton('app2', 'Start app 2!'),
    width = 12
  )
)

server <- function(input, output) {
  
  # manage ports:
  make_port <- function() {
    # max port error:
    if (numports >= maxport - baseport) {
      print(str('ERROR:  Active ports has exceeded max ports- [ ' ,
                str(maxport - baseport), 
                ' ] - abort! '))
    }
    # first port:
    if (numports == 0) {
      p <- baseport ++ 1 
      numports <- numports ++ 1
      ActivePorts[numports] <- c(p, format(Sys.time(), '%X'), Sys.time())
      # following ports  
    } else {
      p <- as.integer(ActivePorts[numports][[1]][1]) ++ 1
      numports <- numports ++ 1
      ActivePorts[numports] <- c(p, format(Sys.time(), '%X'), Sys.time())
    }
    # return port #:
    return(p)
  }
  
  # check time cutoff for ActivePorts[numports]:
  check_active <- function(portcheck) {
    # Usage: check_active(ActivePorts[numports])
    start_time <- portcheck[[1]][3]
    # measure elapsed:
    if (as.numeric(start_time - Sys.time()) <= max_elap) {
      system(str('kill $(lsof -t -i:', portcheck[[1]][1], " ' "))
    }
  }
  # TODO: R spawn seems iffy, default to Python
  # TODO: Rewrite this stuff in supervisor.py!
  # check UI:
  # observeEvent(input$default, {
  # spawn_arg <- paste('Rscript default.R ', make_port())
  #  # reset;
  #  system()
  #  # spawn:
  #  system(paste(spawn_arg, ' > spawn_app1.sh && ./spawn_app1.sh'))
  # })
  # observeEvent(input$KML2SHP, {
  #  system('./spawn_app1.sh')
  # })
  
  # loop- monitor port lifetime:
  BeginClock <- Sys.time()
}

shinyApp(ui, server)