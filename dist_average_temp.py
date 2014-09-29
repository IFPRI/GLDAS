
import arcpy
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace = "D:/Users/cmarciniak/My Documents/GLDAS/GLDAS_MOS025SUBP_3H/"
arcpy.env.overwriteOutput = True





outputFolder = "D:/Users/cmarciniak/My Documents/GLDAS/rasters/"



	
# takes in an array of rasters, outputs one file per day with the average surface temperature
def dailyAverage(rasters , filename):
	outCellStats = CellStatistics( rasters , "MEAN","DATA" )
	outCellStats.save("D:/Users/cmarciniak/My Documents/GLDAS/rasters/"+filename)

def makeRasterArray(files):
	#outputFolder = "D:/Users/cmarciniak/My Documents/GLDAS/rasters/"
	print("Making rasters...")
	rasters=[]
	for file in files:
		print(file)
		tempFile = file[0:12]
		arcpy.MakeNetCDFRasterLayer_md( file , "AvgSurfT_GDS0_SFC", "g0_lon_1","g0_lat_0",tempFile)
		rasters.append(tempFile)
		return rasters
			

def cellStats(rasters):
	print(rasters)
	outputFolder = "D:/Users/cmarciniak/My Documents/GLDAS/rasters/"
	outCellStats = CellStatistics(rasters,"MEAN","DATA")
	outCellStats.save("in_memory/avg_temp")

def resample(inRaster,outRaster):
	arcpy.Resample_management(inRaster,outRaster,.05)

districts = "D:/Users/cmarciniak/My Documents/ArcGIS/2011 Districts MAPS Shape Files/DISTRCT_BDY_geog.shp"


rasters = makeRasterArray(files)

cellStats(rasters)

'''print(outputFolder+"avg_temp/w001001.adf")
arcpy.env.workspace = ""
outZonalStatistics = ZonalStatisticsAsTable(districts,"ID", "D:/Users/cmarciniak/resample.ovr","D:/Users/cmarciniak/zones.dbf")
#outZonalStatistics.save("D:/Users/cmarciniak/My Documents/GLDAS/zones")'''