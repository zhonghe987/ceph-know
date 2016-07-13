import requests
from awsauth import S3Auth
 
#access_key = "8ESWLT47GZW2HZ8NRWZI"
#secret_key = "GLBZWDyJqfvKu5sSZzyhW84RfkAmZOWomoI3eNI2"
server = '192.168.205.43'
access_key =  "9DXOWU1HE84QW0WPE2S3"
secret_key =  "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"
 
url = 'http://%s/admin/bucket?bucket=my_homese' % server
r = requests.get(url, auth=S3Auth(access_key, secret_key, server))
print r.status_code
print r.content
