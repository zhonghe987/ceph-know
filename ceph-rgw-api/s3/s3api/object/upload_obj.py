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
  header,data = {},''
  if method == "put":
     header = {"x-amz-acl": "private"}
     #data = "this is a test ok".encode("utf-8")
     with open("/root/we.tar.gz","r") as f:
          data = f.read()   
  elif method == "post":
     data = '<?xml version="1.0" encoding="UTF-8"?>\
<CompleteMultipartUpload xmlns="http://s3.amazonaws.com/doc/2006-03-01/">\
<Part><PartNumber>1</PartNumber><ETag>df9882babeb3090b736931443b293947</ETag></Part>\
<Part><PartNumber>2</PartNumber><ETag>df9882babeb3090b736931443b293947</ETag></Part>\
<Part><PartNumber>3</PartNumber><ETag>df9882babeb3090b736931443b293947</ETag></Part>\
<Part><PartNumber>4</PartNumber><ETag>df9882babeb3090b736931443b293947</ETag></Part></CompleteMultipartUpload>'
    
  url = "http://%s/%s"%(server,api)
  r = METHOD[method](url, auth=S3Auth(ACCESS_KEY, SECRET_KEY, server),headers = header,data = data)
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
    
    
    
<?xml version="1.0" encoding="UTF-8"?>
<CompleteMultipartUpload xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<MaxParts>1000</MaxParts>
<IsTruncated>false</IsTruncated>
<Owner><ID>testid</ID><DisplayName>test</DisplayName></Owner>
<Part><LastModified>2016-07-07T07:33:33.672Z</LastModified><PartNumber>1</PartNumber><ETag>&quot;2495f27126242e6c020860d5d47353b3&quot;</ETag><Size>17</Size></Part>
<Part><LastModified>2016-07-07T07:33:42.513Z</LastModified><PartNumber>2</PartNumber><ETag>&quot;2495f27126242e6c020860d5d47353b3&quot;</ETag><Size>17</Size></Part>
<Part><LastModified>2016-07-07T07:33:47.054Z</LastModified><PartNumber>3</PartNumber><ETag>&quot;2495f27126242e6c020860d5d47353b3&quot;</ETag><Size>17</Size></Part>
</CompleteMultipartUpload>
