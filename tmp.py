import hmac
from hashlib import sha1
from time import time
import requests
method = 'GET'

host = "http://192.168.189.141:8000/swift"
duration_in_seconds = 6000  # Duration for which the url is valid
expires = int(time() + duration_in_seconds)

path = '/v1/my_names/test.txt'
key = 'abcdefg123456789'

hmac_body = '%s\n%s\n%s' % (method, expires, path)
sig = hmac.new(key, hmac_body, sha1).hexdigest()
print hmac_body
#sig = hmac.new(key, hmac_body, sha1).hexdigest()
rest_uri = "{host}{path}?temp_url_sig={sig}&temp_url_expires={expires}".format(
             host=host, path=path, sig=sig, expires=expires)
r = requests.get(rest_uri)
print r.status_code
print r.content
print rest_uri
