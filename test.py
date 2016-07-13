import unittest
import requests
import untangle
import time
from awsauth import S3Auth
import md5

METHOD = {"put":requests.put,"get":requests.get,"post":requests.post,"delete":requests.delete,"head":requests.head}

def caps(api,method):
    url = "http://%s/admin/user?caps&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print r.content
    return r.status_code

def s3_version(api,method):
    content = ''
    if method == "put":
        content = '<?xml version="1.0" encoding="UTF-8"?><VersioningConfiguration xmlns="http://doc.s3.amazonaws.com/doc/2006-03-01/"><Status>Enabled</Status></VersioningConfiguration>'
        content = bytearray(content,'utf-8')
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),data = content)
    print r.content
    
    print url,method
    print "\n"
    return r.status_code

def s3_obj(api,method,flag = False): 
    header,data = {},''
    m1 = md5.new()
    m1.update(api+str(time.time()))
    url = "http://%s/%s"%(SERVER,api)
    if method == "put":
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  
                  }
        data = "this is a test%s!!!"%m1.hexdigest()
        if flag:
            header["x-amz-copy-source"] =  "s3_object_bucket_0/test_2.txt" 
            r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header)
            return r.status_code
    elif method == "head":
        r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER))
        print r.headers
        print r.content
        return r.status_code
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = data)
    
    print r.content 
    print url,method
    print "\n"
    return r.status_code

def bucket(api,method):
    url = "http://%s/admin/bucket?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print r.content
    print r.headers 
    print url,method
    print "\n"
    return r.status_code

if __name__=="__main__":
   SERVER = "objStor02:7480"
   ADMIN_ACCESS_KEY = "8LQDU10IF59POC91P07A"
   ADMIN_SECRET_KEY = "yjfdVcg1UHPO3M2EoBMoCYhpp3sR2ii615jWk79G"
   USER_ACCESS_KEY =  "U1PEQHZ0I9ZA8QGIKOMZ"
   USER_SECRET_KEY = "tyrwA7x0gINUN8VyM3yjw9H9Qp1ZXYGukoycGDob"
   #for i in range(2):
   #    s3_obj("s3_object_bucket_2/test.txt","put")
   #s3_obj("test_bucket/index.html","head")
   #s3_version("s3_object_bucket_2?versions","get")
   bucket("uid=testid&bucket=s3_object_bucket_4","put")
