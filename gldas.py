
import requests

def download( url ):
	res = requests.get( url )
	file = open( url[263:275]+".nc" , 'wb' ) # characters 263:270 contains datetime information
	file.write( res.content )
	file.close()


f = open("2002019.inp")
text = f.read()
urls = text.split('\n')
for url in urls:
	download( url )


