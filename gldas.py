import glob, time
import requests
import os.path



def download( url ):
	filename = url[274:286]+".nc"
	if os.path.isfile( "GLDAS_MOS025SUBP_3H/"+filename ):
		print("Skipping "+filename)
	else :
		print("Downloading "+filename)
		res = requests.get( url )
		file = open( "GLDAS_MOS025SUBP_3H/"+filename , 'wb' ) # characters 263:270 contains datetime information
		file.write( res.content )
		file.close()
		
def bulkDownload( files ):
	for file in files:
		print("Reading "+file)
		f = open( file )
		text = f.read()
		urls = text.split('\n')
		for url in urls:
			try:
				download( url )
			except requests.exceptions.MissingSchema:
				pass




files = glob.glob("*.inp")

bulkDownload( files )


'''f = open("2002019.2100.inp")
text = f.read()
urls = text.split('\n')
for i in range(5069,5070):
	download( urls[i] )
	time.sleep(1)
'''