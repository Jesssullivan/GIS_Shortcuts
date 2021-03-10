#!/bin/bash
apt install python git gdebi-core gconf2 gconf-service install default-jre default-jdk
R CMD javareconf
apt-get install r-base-dev libgdal-dev libssl-dev libxml2-dev libcurl4-openssl-dev libudunits2-dev
apt update
apt upgrade
apt --fix-broken install
