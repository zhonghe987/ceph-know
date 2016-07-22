import sys
import os
import socket
import unittest
import requests
import untangle
import time 
import hashlib
import base64
from awsauth import S3Auth


ADMIN_ACCESS_KEY = ''
ADMIN_SECRET_KEY = ''

USER_ACCESS_KEY = ''
USER_SECRET_KEY = ''

SERVER = ''

METHOD = {"put":requests.put,"get":requests.get,"post":requests.post,"delete":requests.delete,"head":requests.head}

def user(api,method,flag = False):
    url = "http://%s/admin/user?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print url,method
    print r.content
    
    print "\n"
    if flag:
        return r.json(),r.status_code
    return r.status_code 

def bucket(api,method,flag=False):
    url = "http://%s/admin/bucket?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print url,method
    print r.content
    print "\n"
    if flag:
        return r.status_code,r.json()
    return r.status_code

def s3_bucket(api,method,data = '',header = {},flag = False,ids = False):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = data)
    print url,method
    print r.content
    print r.headers
    print "\n"
    if ids:
        return r.status_code,r.content
    return r.status_code

def s3_obj(api,method,header = {},flag = False): 
    data = ''
    url = "http://%s/%s"%(SERVER,api)
    if method == "put":
        data = "this is a test!!!%s"%api
        if flag:
            header["x-amz-copy-source"] =  "s3_object_bucket_0/test_2.txt" 
            r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header)
            return r.status_code
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = data)
    print url,method
    print r.content
    print r.headers 
    print "\n"
    return r.status_code


class TesRgwApi(unittest.TestCase):
   
    def test_001_s3_create_bucket(self):
       
       header = {"x-amz-acl": "public-read-write"}
       self.assertEqual(s3_bucket('s3_object_bucket_0',"put",header = header),200)
    
    def test_002_s3_create_obj(self):
        api = "s3_object_bucket_0/wewe/test_dir.txt"
        self.assertEqual(s3_obj(api,"put"),200)
    
    def test_003_s3_create_obj(self):
        api = "s3_object_bucket_0/test_4.txt"
        self.assertEqual(s3_obj(api,"put"),200)

    def test_004_s3_get_obj(self):
        api = "s3_object_bucket_0/test_4.txt"
        self.assertEqual(s3_obj(api,"get"),200) 
   
    def test_005_s3_get_obj(self):
        api = "s3_object_bucket_0/test_4.txt"
        self.assertEqual(s3_obj(api,"get"),200)

    def test_006_delete_obj(self):
        self.assertEqual(bucket("object&bucket=s3_object_bucket_0&object=test_4.txt","delete"),200)    
        self.assertEqual(bucket("object&bucket=s3_object_bucket_0&object=wewe/test_dir.txt","delete"),200)    

    def test_007_s3_delete_bucket(self):
        self.assertEqual(bucket("bucket=s3_object_bucket_0&purge-objects=True","delete"),200)
     
    def test_008_s3_delete_bucket(self):
        self.assertEqual(s3_bucket("s3_object_bucket_0","delete"),404)

    def test_009_delete_user(self):
        for i in ["dir_test","Admin_api"]:
            self.assertEqual(user("uid=%s&purge-data=True"%i,"delete"),200)

if __name__ == "__main__":
    
   
    hostName = socket.gethostname()
    SERVER = "%s:8000"%hostName
    out =   os.popen("/root/ceph/src/radosgw-admin user create --uid=Admin_api --display_name=api --caps='users=*;usage=*;buckets=*;metadata=*;zone=*'")
    result = out.readlines()[11:14]
    print result
    ADMIN_ACCESS_KEY = result[0].split('"')[3]
    ADMIN_SECRET_KEY = result[1].split('"')[3]
    info = user("uid=dir_test","get",True)
    if info[1] == 404:
        info = user("uid=dir_test&display-name=test","put",True)
        if info[1] != 200:
            sys.exit(1)
        USER_ACCESS_KEY = info[0]["keys"][0]["access_key"]
        USER_SECRET_KEY = info[0]["keys"][0]["secret_key"]
    elif info[1] == 200:
        USER_ACCESS_KEY = info[0]["keys"][0]["access_key"]
        USER_SECRET_KEY = info[0]["keys"][0]["secret_key"]
    else:
        print info
    #print USER_ACCESS_KEY
    #print USER_SECRET_KEY
    unittest.main()
