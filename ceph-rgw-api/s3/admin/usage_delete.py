import requests
from awsauth import S3Auth
import  sys


#access_key = "8ESWLT47GZW2HZ8NRWZI"
#secret_key = "GLBZWDyJqfvKu5sSZzyhW84RfkAmZOWomoI3eNI2"
#server = '192.168.205.43'
access_key =  "9DXOWU1HE84QW0WPE2S3"
secret_key =  "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"
METHOD = {"put":requests.put,"get":requests.get,"post":requests.post,"delete":requests.delete,"head":requests.head}

 
#url = 'http://%s/admin/usage?uid=testid' % server
#r = requests.delete(url, auth=S3Auth(access_key, secret_key, server))
#print r.status_code
#print r.content


def usage(server,api,method):
  
  url = "http://%s/admin/usage?%s"%(server,api)
  r = METHOD[method](url, auth=S3Auth(access_key, secret_key, server))
  print r.status_code
  print r.content
  
if __name__=="__main__":
    if len(sys.argv) < 3:
       sys.exit(0)
    server = sys.argv[1]
	api = sys.argv[2]
	method = sys.argv[3]
	usage(server,api,method)