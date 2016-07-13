import requests
from awsauth import S3Auth
import  sys


#access_key = "8ESWLT47GZW2HZ8NRWZI"
#secret_key = "GLBZWDyJqfvKu5sSZzyhW84RfkAmZOWomoI3eNI2"
#server = '192.168.205.43'

#ACCESS_KEY  =  "9DXOWU1HE84QW0WPE2S3"
#SECRET_KEY  =  "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"
ACCESS_KEY  = "D673C77LPU5S1EICB3KL"
SECRET_KEY  = "7WC81mElj1Y2dmGUupnL3DJwXxJEZLl1AXZ4gEcL"
METHOD = {"put":requests.put,"get":requests.get,"post":requests.post,"delete":requests.delete,"head":requests.head}

def user(server,api,method):
  content = ''
  if method == "put":
    content = '<?xml version="1.0" encoding="UTF-8"?><VersioningConfiguration xmlns="http://doc.s3.amazonaws.com/doc/2006-03-01/"><Status>Enabled</Status></VersioningConfiguration>'
    content = bytearray(content,'utf-8')
  url = "http://%s/%s"%(server,api)
  r = METHOD[method](url, auth=S3Auth(ACCESS_KEY, SECRET_KEY, server),data = content)
  print r.status_code
  print r.content
  
if __name__=="__main__":
    print sys.argv
    if len(sys.argv) < 4:
       sys.exit(0)
    #print sys.argv
    server = sys.argv[1]
    api = sys.argv[2]
    method = sys.argv[3]
    user(server,api,method)
