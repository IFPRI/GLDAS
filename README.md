GLDAS
=====

This repository contains code and information for downloading and processing raster weather data from NASA's Global Land Data Assimilation System using the Simple Subset Wizard.
http://hydro1.sci.gsfc.nasa.gov/dods/GLDAS_NOAH025_3H.020.info

Requirements
=====
python, arcpy, R
the requests module for python. pip install requests

Steps
=====

First select the desired dataset, date range, and spatial bounding box.
Select netCDF as the format and choose the desired variables. Click Subset Selected Data.
View subset results
Right click the link to get list of URLs for this subset in a file and save it to your computer.

run python gldas.py

The script will then iterate through the urls in the file and download them to your computer. If downloading many files the connection may time out

dist_avg_temp.py creates raster layers from the downloaded files and computes the average temperature for districts taken from a shapefile.

dbf_to_csv.R loops through the dbf output of dist_avg_temp.py and converts the files to csv



