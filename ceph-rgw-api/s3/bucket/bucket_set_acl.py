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
access_key =  "XT7E864IPGGT067516F6",
secret_key =  "TEZcOgRVAPWWlCkHe4i8cRjA2HC3EEFdPNZHclLD"
timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
hstr = ''
hstr += 'PUT\n'
hstr += '\n'
hstr += '\n'
hstr += timestr + '\n'
hstr += '/my_infos?acl'
print('hstr:%s' % (hstr,))

key = bytearray(secret_key, 'utf-8')
hres = hmac.new(key, hstr.encode('utf-8'), hashlib.sha1).digest()
print('type:%s' % (type(hres, )))

hres = base64.b64encode(hres)

acl = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xuwenping</ID><DisplayName>ceph xuwenping</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xuwenping</ID><DisplayName>ceph xuwenping</DisplayName></Grantee><Permission>FULL-CONTROL</Permission></Grant></AccessControlList></AccessControlPolicy>'
acl =  bytes(acl)
hres = hres.decode('utf-8')
print('hres:%s' % (hres,))
aws = 'AWS %s:%s'%(access_key[0],hres)
print aws
header = {"Host":"192.168.205.43:80","Date":timestr,"Authorization":aws,}
#header = {"Date":timestr,"Authorization":aws,"x-amz-acl": "public-read-write"}
req = requests.put(url = 'http://192.168.205.43:80/my_infos?acl',
                   headers = header,data=acl)
print req.status_code
print req.content
