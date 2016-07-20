import urllib
import requests
import hmac
import hashlib
import base64 
import datetime


#access_key = "9DXOWU1HE84QW0WPE2S3",
#secret_key = "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"
#access_key =  "D673C77LPU5S1EICB3KL",
#secret_key = "7WC81mElj1Y2dmGUupnL3DJwXxJEZLl1AXZ4gEcL"
access_key =  "K2IO8I2B9JQJIB8FF0G3"
secret_key =  "1A5jBwOsvM8MCD9zjb2AcQadA6ussLF3QnZDXE2G"

with open("/root/anaconda-ks.cfg","r") as  f:
     content = f.read()


m = hashlib.md5()
m.update(content)
md5value = base64.b64encode(m.digest()).decode('utf-8')

timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
hstr = ''
hstr += 'PUT\n'
hstr += md5value + '\n'
hstr += 'text/plain\n'
hstr += timestr + '\n'
hstr += '/s3_object_bucket/ac.conf'
print('hstr:%s' % (hstr,))

key = bytearray(secret_key, 'utf-8')
hres = hmac.new(key, hstr.encode('utf-8'), hashlib.sha1).digest()
print('type:%s' % (type(hres, )))

hres = base64.b64encode(hres)
hres = hres.decode('utf-8')
print('hres:%s' % (hres,))
aws = 'AWS %s:%s'%(access_key,hres)
print aws
header = {"Host":"localhost:8000","Date":timestr,"Authorization":aws,"Content-MD5":md5value,"Content-Type":"text/plain"}
#header = {"Date":timestr,"Authorization":aws,"x-amz-acl": "public-read-write"}
req = requests.put(url = 'http://localhost:8000/s3_object_bucket/ac.conf',
                   headers = header,data=content)
print req.status_code
print req.content

#--------------get--------------
timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
hstr = ''
hstr += 'GET\n'
hstr += '\n'
hstr += '\n'
hstr += timestr + '\n'
hstr += '/s3_object_bucket/ac.conf'
print('hstr:%s' % (hstr,))

key = bytearray(secret_key, 'utf-8')
hres = hmac.new(key, hstr.encode('utf-8'), hashlib.sha1).digest()
print('type:%s' % (type(hres, )))

hres = base64.b64encode(hres)

aws = 'AWS %s:%s'%(access_key,hres)
header = {"Host":"localhost:8000","Date":timestr,"Authorization":aws}
req = requests.get(url = 'http://localhost:8000/s3_object_bucket/ac.conf',
                   headers = header)
print req.status_code
print req.content
