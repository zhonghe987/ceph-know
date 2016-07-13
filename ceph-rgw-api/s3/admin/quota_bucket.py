import requests
from awsauth import S3Auth
 
#access_key = "8ESWLT47GZW2HZ8NRWZI"
#secret_key = "GLBZWDyJqfvKu5sSZzyhW84RfkAmZOWomoI3eNI2"
server = '192.168.205.43'
access_key =  "9DXOWU1HE84QW0WPE2S3"
secret_key =  "9n3sJDW4mPKMlNIkC833Xug4vO7FjkrUIU8B2Uzv"
content = '{"enabled":true,"max_size_kb":1000000,"max_objects":1000}'
content = bytes(content) 
url = 'http://%s/admin/user?quota&uid=testid&quota-type=bucket' % server
r = requests.put(url, auth=S3Auth(access_key, secret_key, server),data=content)
print r.status_code
print r.content


<?xml version="1.0" encoding="UTF-8"?>
<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<Owner><ID>testid</ID><DisplayName>testid_ui</DisplayName></Owner>
<Buckets>
<Bucket><Name>my_bucket</Name><CreationDate>2016-06-22T06:23:17.000Z</CreationDate></Bucket>
<Bucket><Name>rgw_admin</Name><CreationDate>2016-06-27T05:47:43.000Z</CreationDate></Bucket>
<Bucket><Name>rgw_admin_index</Name><CreationDate>2016-06-27T05:47:50.000Z</CreationDate></Bucket>
</Buckets>
</ListAllMyBucketsResult>
