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


access_key = "9DXOWU1HE84QW0WPE2S3",
secret_key = "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"

timestr = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
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
header = {"Host":"192.168.205.43:80","Date":timestr,"Authorization":aws}
req = requests.put(url = 'http://192.168.205.43/admin/user?format=json&uid=eleme&subuser=eleme_qsf&gen-subuser=eleme_qsf&access=full',
                   headers = header,)
print req.json()
