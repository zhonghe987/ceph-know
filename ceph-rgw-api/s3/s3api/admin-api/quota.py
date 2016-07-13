import requests
from awsauth import S3Auth
import  sys


#access_key = "8ESWLT47GZW2HZ8NRWZI"
#secret_key = "GLBZWDyJqfvKu5sSZzyhW84RfkAmZOWomoI3eNI2"
#server = '192.168.205.43'

ACCESS_KEY  =  "9DXOWU1HE84QW0WPE2S3"
SECRET_KEY  =  "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"
METHOD = {"put":requests.put,"get":requests.get,"post":requests.post,"delete":requests.delete,"head":requests.head}

def quota(server,api,method):
  content = ''
  if method == 'put':
     content = bytearray('{"enabled":true,"max_size_kb":1000000,"max_objects":100}','utf-8') 

  url = "http://%s/admin/user?%s"%(server,api)
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
    quota(server,api,method)
