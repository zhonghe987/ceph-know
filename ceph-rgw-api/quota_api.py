#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

#easy_install requests-aws
#easy_install requests
#easy_install untangle

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

"""
 rgw enable usage log = true
 rgw usage log tick interval = 30
 rgw usage log flush threshold = 1024
 rgw usage max shards = 32
 rgw usage max user shards = 1
"""

def usage(api,method):
    url = "http://%s/admin/usage?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print url,method
    print r.content
    print "\n"
    return r.status_code 

def user(api,method,flag = False):
    url = "http://%s/admin/user?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print url,method
    print r.content
    
    print "\n"
    if flag:
        return r.json(),r.status_code
    return r.status_code 

def subuser(api,method):
    url = "http://%s/admin/user?subuser&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print url,method
    print r.content
    print "\n"
    return r.status_code 

def keys(api,method):
    url = "http://%s/admin/user?key&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print url,method
    print r.content
    print "\n"
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

def caps(api,method):
    url = "http://%s/admin/user?caps&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print url,method
    print r.content
    print "\n"
    return r.status_code

def quota(api,method,data = ''):
    
    url = "http://%s/admin/user?quota&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER),data = data)
    print url,method
    print r.content
    print "\n"
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

def s3_version(api,method):
    content = ''
    if method == "put":
        content = '<?xml version="1.0" encoding="UTF-8"?><VersioningConfiguration xmlns="http://doc.s3.amazonaws.com/doc/2006-03-01/"><Status>Enabled</Status></VersioningConfiguration>'
        content = bytearray(content,'utf-8')
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),data = content)
    print url,method
    print r.content
    print "\n"
    return r.status_code

def s3_acl(api,method,data = ''):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),data = data)
    print url,method 
    print r.content  
    print "\n"
    return r.status_code

def s3_upload(api,method):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER))
    print url,method
    print r.content
    print "\n"
    return r.status_code


def s3_obj(api,method,header = {},flag = False): 
    data = ''
    url = "http://%s/%s"%(SERVER,api)
    if method == "put":
        with open("/root/api/rgw.log","r") as f:
            data = f.read(1024*1024)
        if flag:
            header["x-amz-copy-source"] =  "s3_object_bucket_0/test_2.txt" 
            r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header)
            return r.status_code
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = bytearray(data))
    print url,method
    print r.content
    print r.headers 
    print "\n"
    return r.status_code

def s3_obj_acl(api,method):
    header,data = {},''
    if method == "put":
        #header = {"x-amz-acl": "private"}
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>s3_api</ID><DisplayName>s3_api_ui</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>s3_api</ID><DisplayName>s3_api_ui</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = data)
    print url,method
    print r.content
    print "\n"
    return r.status_code

def s3_request(api,method,header = {},data = ""):
    url = "http://%s/%s"%(SERVER,api)
    if method == "put":
        with open("/root/api/cent.iso","r") as f:
            data = f.read()
        r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = data)
    else:
        r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),data = data)
    print url,method
    #print r.content
    print "\n"
    return r.status_code,r.content
    
    
def s3_obj_mult():
    """
    Initiates a multi-part upload process
    POST /{bucket}/{object}?uploads
    """
    code,info = s3_request("s3_object_bucket_0/disk.img?uploads","post")
    if code != 200:
        return code
    obj = untangle.parse(info)
    uploadID = obj.InitiateMultipartUploadResult.UploadId.cdata
    
    """
    Adds a part to a multi-part upload.
    PUT /{bucket}/{object}?partNumber=&uploadId={upload-id}
    """
    for i in range(5):
        code,info =  s3_request("s3_object_bucket_0/disk.img?partNumber=%s&uploadId=%s"%(i,uploadID),"put")
        if code != 200:
            return code
    """
    Specify the uploadId subresource and the upload ID to list the parts of a multi-part upload.
    GET /{bucket}/{object}?uploadId={upload-id}
    """
    code,info = s3_request("s3_object_bucket_0/disk.img?uploadId=%s"%uploadID,"get")
    if code != 200:
        return code
    info = info.replace("ListPartsResult","CompleteMultipartUpload")
    
    """
    Assembles uploaded parts and creates a new object
    POST /{bucket}/{object}?uploadId= HTTP/1.1
    """
    code,info = s3_request("s3_object_bucket_0/disk.img?uploadId=%s"%uploadID,"post",data = info)
    if code != 200:
        return code
    
    """
    ABORT MULTIPART UPLOAD
    DELETE /{bucket}/{object}?uploadId=
    """
    code,info = s3_request("s3_object_bucket_0/disk.img?uploadId=%s"%uploadID,"delete")
    if code != 204:
        return code
    return code


class TesRgwApi(unittest.TestCase):
    
    def test_001_s3_create_bucket(self):
        for i  in range(3):
            header = {"x-amz-acl": "public-read-write"}
            self.assertEqual(s3_bucket('s3_object_bucket_%s'%i,"put",header = header),200)
    
    
    def test_002_get_user_quota(self):
        self.assertEqual(quota("uid=quota_api&quota-type=user","get"),200)
        
    """
    Setting User Quota
    PUT /admin/user?quota&uid=<uid>&quota-type=user
    @uid
    """
    def test_003_set_user_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":3072,"max_objects":3}','utf-8') 
        self.assertEqual(quota("uid=quota_api&quota-type=user","put",data),200)
        
    """
    Getting Bucket Quota
    GET /admin/user?quota&uid=<uid>&quota-type=bucket
    @uid
    """
    def test_004_get_bucket_quota(self):
        self.assertEqual(quota("uid=quota_api&quota-type=bucket","get"),200)
    
    """
    Setting Bucket Quota
    PUT /admin/user?quota&uid=<uid>&quota-type=bucket
    @uid
    """
    def test_005_set_bucket_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":2048,"max_objects":1}','utf-8') 
        self.assertEqual(quota("uid=quota_api&quota-type=bucket","put",data),200)
    
    def test_006_s3_create_obj(self):
            header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
            api = "s3_object_bucket_0/test_0.txt"
            self.assertEqual(s3_obj(api,"put",header = header),200)
    
    #def test_007_set_bucket_quota(self):
    #    data = bytearray('{"enabled":true,"max_size_kb":0,"max_objects":1}','utf-8') 
    #    self.assertEqual(quota("uid=quota_api&quota-type=bucket","put",data),200)
        
    def test_008_s3_create_obj(self):
            header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
            api = "s3_object_bucket_1/test_0.txt"
            self.assertEqual(s3_obj(api,"put",header = header),200)
            
    def test_009_s3_create_obj(self):     
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_0/test_1.txt"
        self.assertEqual(s3_obj(api,"put",header = header),403)
            
    def test_010_set_bucket_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":2048,"max_objects":2}','utf-8') 
        self.assertEqual(quota("uid=quota_api&quota-type=bucket","put",data),200)
        
    def test_011_s3_create_obj(self):     
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_0/test_1.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
        
    def test_012_s3_create_obj(self):     
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_1/test_1.txt"
        self.assertEqual(s3_obj(api,"put",header = header),403)
        
    
    
    def test_013_set_user_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":5000,"max_objects":10}','utf-8') 
        self.assertEqual(quota("uid=quota_api&quota-type=user","put",data),200)
        
        
    def test_014_s3_create_obj(self):     
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_1/test_2.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
        
    
    def test_015_set_bucket_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":5000,"max_objects":10}','utf-8') 
        self.assertEqual(quota("uid=quota_api&quota-type=bucket","put",data),200)
        
            
    def test_016_s3_create_obj(self):    
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_0/test_2.txt"
        self.assertEqual(s3_obj(api,"put",header = header),403)
        
    def test_017_s3_create_obj(self):    
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_1/test_3.txt"
        self.assertEqual(s3_obj(api,"put",header = header),403)
        
    
        
    def test_018_set_user_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":4000,"max_objects":20}','utf-8') 
        self.assertEqual(quota("uid=quota_api&quota-type=user","put",data),200)
        
    def test_019_s3_create_obj(self):    
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_0/test_3.txt"
        self.assertEqual(s3_obj(api,"put",header = header),403)
        
    def test_020_s3_get_obj(self):    
        api = "s3_object_bucket_0/test_1.txt"
        self.assertEqual(s3_obj(api,"get"),200)
        
    
    def test_021_s3_del_obj(self):    
        api = "s3_object_bucket_0/test_2.txt"
        self.assertEqual(s3_obj(api,"delete"),204)
        
        
    def test_022_s3_create_obj(self):    
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_0/test_2.txt"
        self.assertEqual(s3_obj(api,"put",header = header),403)
        
    def test_023_s3_del_bucket(self):    
        self.assertEqual(bucket("bucket=s3_object_bucket_0&purge-objects=True","delete"),200)
        
    
    def test_024_s3_create_obj(self):    
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_1/test_4.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
    
    def test_025_create_user(self):
        self.assertEqual(user("uid=other_api&display-name=api","put"),200)
        #self.assertEqual(subuser("uid=quota_api&subuser=foo_api&access=full&ecret-key=asdfsdfsdf&key-type=s3&access-key=123123123","put"),200)
        os.popen("/root/ceph/src/radosgw-admin subuser create --uid=quota_api --subuser=sub_quota --key-type=s3 --access=full  --access-key=r12234556")
    
    def test_026_set_user_quota(self):
        info = user("uid=quota_api","get",True)
        sub_ACCESS_KEY = info[0]["keys"][1]["access_key"]
        sub_SECRET_KEY = info[0]["keys"][1]["secret_key"]
        api = "uid=quota_api&quota-type=user"
        url = "http://%s/admin/user?quota&%s&format=json"%(SERVER,api)
        data = bytearray('{"enabled":true,"max_size_kb":6000,"max_objects":20}','utf-8') 
        r = requests.put(url, auth=S3Auth(sub_ACCESS_KEY, sub_SECRET_KEY, SERVER),data = data)
        print url
        print r.content
        print "\n"
        self.assertEqual(r.status_code,403)
    

    def test_027_set_user_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":6000,"max_objects":20}','utf-8') 
        self.assertEqual(quota("uid=quota_api&quota-type=user","put",data),200)
    
    def test_028_set_create_obj(self):
        info = user("uid=other_api","get",True)
        oth_ACCESS_KEY = info[0]["keys"][0]["access_key"]
        oth_SECRET_KEY = info[0]["keys"][0]["secret_key"]
        with open("/root/api/rgw.log","r") as f:
            data = f.read(1024*1024)
        api = "s3_object_bucket_1/test_6.txt"
        url = "http://%s/%s"%(SERVER,api)
        r = requests.put(url, auth=S3Auth(oth_ACCESS_KEY, oth_SECRET_KEY, SERVER),data = data)
        print url
        print r.content
        print "\n"
        self.assertEqual(r.status_code,200)
        
    def test_029_sub_create_obj(self):
        info = user("uid=quota_api","get",True)
        sub_ACCESS_KEY = info[0]["keys"][1]["access_key"]
        sub_SECRET_KEY = info[0]["keys"][1]["secret_key"]
        print sub_ACCESS_KEY
        print sub_SECRET_KEY
        api = "s3_object_bucket_1/test_5.txt"
        url = "http://%s/%s"%(SERVER,api)
        with open("/root/api/rgw.log","r") as f:
            data = f.read(1024*1024)
        r = requests.put(url, auth=S3Auth(sub_ACCESS_KEY, sub_SECRET_KEY, SERVER),data = data)
        print url
        print r.content
        print "\n"
        self.assertEqual(r.status_code,403)
        
    def test_030_set_bucket_quota(self):
        data = bytearray('{"enabled":true,"max_size_kb":4,"max_objects":1,"bucket":"s3_object_bucket_2"}','utf-8')
        self.assertEqual(quota("uid=quota_api&quota-type=bucket","put",data),200)
    
    def test_031_etg_bucket_quota(self):
        self.assertEqual(quota("uid=quota_api&quota-type=bucket&bucket=s3_object_bucket_2","get"),200)
    
    def test_032_s3_create_obj(self):    
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_2/test_4.txt"
        url = "http://%s/%s"%(SERVER,api)
        data = bytearray('{"enabled":true,"max_size_kb":4,"max_objects":1,"bucket":"s3_object_bucket_2"}','utf-8')
        r = requests.put(url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = bytearray(data))
        print url,"put"
        print r.content
        print r.headers 
        print "\n"
        self.assertEqual(r.status_code,200)
        
    def test_033_s3_create_obj(self):    
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_2/test_0.txt"
        url = "http://%s/%s"%(SERVER,api)
        data = bytearray('{"enabled":true,"max_size_kb":4,"max_objects":1,"bucket":"s3_object_bucket_2"}','utf-8')
        r = requests.put(url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = bytearray(data))
        print url,"put"
        print r.content
        print r.headers 
        print "\n"
        self.assertEqual(r.status_code,403)
        
        
    def test_034_s3_del_user(self):
        self.assertEqual(user("uid=quota_api&purge-data=True","delete"),200)
        
if __name__ == "__main__":
    hostName = socket.gethostname()
    SERVER = "%s:8000"%hostName
    out =   os.popen("/root/ceph/src/radosgw-admin user create --uid=Admin_api --display_name=api --caps='users=*;usage=*;buckets=*;metadata=*;zone=*'")
    result = out.readlines()[11:14]
    print result
    ADMIN_ACCESS_KEY = result[0].split('"')[3]
    ADMIN_SECRET_KEY = result[1].split('"')[3]
    info = user("uid=quota_api","get",True)
    if info[1] == 404:
        info = user("uid=quota_api&display-name=test","put",True)
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
