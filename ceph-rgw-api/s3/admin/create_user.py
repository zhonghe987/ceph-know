#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
#from urllib2 import Request
#from urllib2 import urlopen
#from urllib.request import Request
import requests
import hmac
import hashlib
import base64 
import datetime

#access_key = 'Z2ETKC4RQFTR4XBQ1A72'
#secret_key = 'vqdQGtmruGW855mduffA8lsLx+ot9iXIb9QTtT2I'
access_key = "9DXOWU1HE84QW0WPE2S3",
secret_key = "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"
#req = requests.Request('http://192.168.205.43/admin/user?uid=eleme&display-name=eleme',
#            method = 'PUT')

timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

#req.add_header('Host', '192.168.205.43')
#req.add_header('Date', timestr) 

hstr = ''
hstr += 'PUT\n'
hstr += '\n'
hstr += '\n'
hstr += timestr + '\n'
hstr += '/admin/user'
print('hstr:%s' % (hstr,))

key = bytearray(secret_key, 'utf-8')
hres = hmac.new(key, hstr.encode('utf-8'), hashlib.sha1).digest()
print('type:%s' % (type(hres, )))

hres = base64.b64encode(hres)

hres = hres.decode('utf-8')
print('hres:%s' % (hres,))
aws = 'AWS %s:%s'%(access_key[0],hres)
print aws
#req.add_header('Authorization', 'AWS ' + access_key + ':' + hres)
req = requests.Request(url = 'http://192.168.205.43/admin/user?uid=eleme&display-name=eleme',
            method = 'PUT',
            headers = {"Host":"192.168.205.43:80","Date":timestr,"Authorization":aws},
            )
r =  req.prepare()
s = requests.Session()
print s.send(r)

#with urllib.request.urlopen(req) as f:
#    print(f.read().decode('utf-8'))
