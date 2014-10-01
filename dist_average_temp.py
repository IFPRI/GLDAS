
import arcpy
from arcpy.sa import *
import glob, os, time
import multiprocessing

arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace = "D:/Users/cmarciniak/tables"
arcpy.env.overwriteOutput = True



outputFolder = "D:/Users/cmarciniak/My Documents/GLDAS/rasters/"
tables = "D:/Users/cmarciniak/My Documents/GLDAS/tables/"


	
# takes in an array of rasters, outputs one file per day with the average surface temperature
def dailyAverage(rasters , filename):
	outCellStats = CellStatistics( rasters , "MEAN","DATA" )
	outCellStats.save("D:/Users/cmarciniak/My Documents/GLDAS/rasters/"+filename)

def makeRasterArray(files):
	#outputFolder = "D:/Users/cmarciniak/My Documents/GLDAS/rasters/"
	print("Making rasters...")
	rasters=[]
	for file in files:
		print("Making raster from "+file)
		tempFile = file[0:12]
		arcpy.MakeNetCDFRasterLayer_md( file , "AvgSurfT_GDS0_SFC", "g0_lon_1","g0_lat_0",tempFile)
		rasters.append(tempFile)
	return rasters
			

def cellStats(rasters):
	print(rasters)
	outputFolder = "D:/Users/cmarciniak/My Documents/GLDAS/rasters/"
	outCellStats = CellStatistics(rasters,"MEAN","DATA")
	try:
		outCellStats.save("in_memory/avg_temp")
	except RuntimeError:
		#os.rmdir(outputFolder+"avg_temp")
		outCellStats.save("in_memory/avg_temp")
	#arcpy.Delete_management("in_memory")

def deleteCellStats(rasters):
	for raster in rasters:
		arcpy.Delete_management(raster)

def resample(inRaster,outRaster):
	if os.path.isdir(outRaster):
		print("Removing "+outRaster)
		#os.rm("D:/Users/cmarciniak/My Documents/GLDAS/rasters/resample.aux.xml")
		#shutil.rmtree(outRaster)
		arcpy.Resample_management(inRaster,outRaster,.05)
	else:
		print("Resampling...")
		arcpy.Resample_management(inRaster,outRaster,.05)
	print("Done")

def ncFileIterator():
	files = glob.glob("*.nc")
	files.sort()
	rasters = []
	temp = []
	for i in range ( 0,len(files)-1 ):
		if files[i][0:7] == files[i+1][0:7]:
			print(files[i][0:7])
			temp.append(files[i])
		else:
			print("Done")
			temp.append(files[i])
			rasters.append(temp)
			temp = []
	return rasters
	



		
def mainLoop(ncFiles):
	districts = "D:/Users/cmarciniak/My Documents/ArcGIS/2011 Districts MAPS Shape Files/DISTRCT_BDY_geog.shp"
	#ncFiles = ncFileIterator()
	rasters = []
	for nc in ncFiles:
		day = nc[0][0:7]
		if(os.path.isfile("D:/Users/cmarciniak/tables/GLDAS_"+day+".dbf")):
			print("Skipping "+day+".dbf")	
			pass	
		else:
			rasters = makeRasterArray(nc)
			cellStats(rasters)
			print(outputFolder)
			resample("in_memory/avg_temp","in_memory/resample")
			outZonalStatistics = ZonalStatisticsAsTable(districts,"ID", "in_memory/resample","D:/Users/cmarciniak/tables/GLDAS_"+nc[0][0:7]+".dbf")
			deleteCellStats(rasters)
			arcpy.Delete_management("in_memory")
			#arcpy.Delete_management(outZonalStatistics)
			#del rasters

def f(ncFiles):
	districts = "D:/Users/cmarciniak/My Documents/ArcGIS/2011 Districts MAPS Shape Files/DISTRCT_BDY_geog.shp"
	rasters = makeRasterArray(ncFiles)
	cellStats(rasters)
	resample("in_memory/avg_temp","in_memory/resample")
	outZonalStatistics = ZonalStatisticsAsTable(districts,"ID", "in_memory/resample","D:/Users/cmarciniak/tables/GLDAS_"+ncFiles[0][0:7]+".dbf")


ncFiles = ncFileIterator()

'''if __name__== '__main__':
	pool = multiprocessing.Pool(processes=4)
	result = pool.map(f,ncFiles,4)
	pool.close()
	pool.join()
'''
mainLoop(ncFiles) 

#rasters = makeRasterArray(files)
#cellStats(rasters)
#print(outputFolder+"avg_temp/w001001.adf")
#arcpy.env.workspace = ""
#outZonalStatistics = ZonalStatisticsAsTable(districts,"ID", "D:/Users/cmarciniak/resample4","D:/Users/cmarciniak/zones4.dbf")
#outZonalStatistics.save("D:/Users/cmarciniak/My Documents/GLDAS/zones")