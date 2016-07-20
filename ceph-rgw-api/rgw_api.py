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

def quota(api,method):
    contents = ''
    if method == 'put':
        contents = bytearray('{"enabled":true,"max_size_kb":1000000,"max_objects":100}','utf-8') 
    url = "http://%s/admin/user?quota&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER),data = contents)
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
    
    """
    Create a new user.
    PUT /admin/user?format=json HTTP/1.1
    @uid
    @display-name
    """
    def test_001_create_user(self): 
        self.assertEqual(user("uid=rgw_api&display-name=api","put"),200) 
        
    def test_002_create_user(self): 
        self.assertEqual(user("uid=rgw_api_1&display-name=api&email=134@163.com","put"),200)
        
    def test_003_create_user(self): 
        self.assertEqual(user("uid=rgw_api_2&display-name=api&access-key=ABCD0EF12GHIJ2K34LMN","put"),200)
    
    def test_004_create_user(self): 
        self.assertEqual(user("uid=rgw_api_3&display-name=api&secret-key=qwertyuiop123456","put"),200)
        
    def test_005_create_user(self): 
        self.assertEqual(user("uid=rgw_api_4&display-name=api&user-caps=usage=read,write;users=read","put"),200)
        
    def test_006_create_user(self): 
        self.assertEqual(user("uid=rgw_api_5&display-name=api&generate-key=True","put"),200)
    
    def test_007_create_user(self): 
        self.assertEqual(user("uid=rgw_api_6&display-name=api&max-buckets=3","put"),200)
    
    def test_008_create_user(self): 
        self.assertEqual(user("uid=rgw_api_7&display-name=api&suspended=True","put"),200)
    
    def test_009_create_user(self): 
        self.assertEqual(user("uid=rgw_api_5&display-name=api&generate-key=True","put"),200)
        
    def test_010_create_user(self): 
        self.assertEqual(user("uid=rgw_api_8&display-name=api&key-type=swift","put"),403)
    
    def test_011_create_user(self): 
        self.assertEqual(user("uid=rgw_api_9&display-name=api&key-type=s3&access-key=a123456789&secret-key=qwertyuio&user-caps=buckets=*&max-buckets=4&suspended=True","put"),200)
    
    """
    Create a new subuser 
    PUT /admin/user?subuser&format=json HTTP/1.1
    @uid
    @subuser 
    @gen-subuser
    """
    def test_012_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&access=read","put"),200)
    
    def test_013_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api_1&subuser=s3_api&access=readwrite","put"),200)
    
    def test_014_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api_3&subuser=s3_api&secret-key=rewq12345","put"),200)
        
    def test_015_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api_2&subuser=s3_api&key-type=swift","put"),200)
        
    def test_016_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api_6&subuser=s3_api&gen-subuser=sub_foo","put"),200)
        
    def test_017_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api_2&subuser=s3_api_1&generate-secret=True","put"),200)
    
    def test_018_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api_4&subuser=s3_api&generate-secret=True","put"),200)
    
    def test_019_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api_7&subuser=s3_api&generate-secret=True","put"),200)
    
    """
    Creates a new bucket.
    PUT /{bucket}
    """
    def test_020_s3_create_bucket(self):
        for i  in range(5):
            header = {"x-amz-acl": "public-read-write"}
            self.assertEqual(s3_bucket('s3_object_bucket_%s'%i,"put",header = header),200)
            
    def test_021_s3_create_bucket(self):
        header = {"x-amz-acl": "private"}
        self.assertEqual(s3_bucket('s3_object_bucket_private',"put",header =header ),200)
    
    def test_022_s3_create_bucket(self):
        header = {"x-amz-acl": "public-read"}
        self.assertEqual(s3_bucket('s3_object_bucket_public_read',"put",header =header ),200)
    
    def test_023_s3_create_bucket(self):
        header = {"x-amz-acl": "authenticated-read"}
        self.assertEqual(s3_bucket('s3_object_bucket_authenticated_read',"put",header =header ),200)
    
    def test_024_s3_create_bucket(self):
        header = {"x-amz-acl": "public-read-write"}
        self.assertEqual(s3_bucket('s3_object_bucket_public_read',"put",header = header),200)
        
    """
    ENABLE/SUSPEND BUCKET VERSIONING
    PUT  /{bucket}?versioning
    """
    def test_025_s3_set_bucket_version(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><VersioningConfiguration xmlns="http://doc.s3.amazonaws.com/doc/2006-03-01/"><Status>Enabled</Status></VersioningConfiguration>'
        self.assertEqual(s3_bucket("s3_object_bucket_0?versioning","put",data = data),200)
           
    def test_026_s3_set_bucket_version(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><VersioningConfiguration xmlns="http://doc.s3.amazonaws.com/doc/2006-03-01/"><Status>Suspended</Status></VersioningConfiguration>'
        self.assertEqual(s3_bucket("s3_object_bucket_4?versioning","put",data = data),200)
    
    def test_027_s3_set_bucket_version(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><VersioningConfiguration xmlns="http://doc.s3.amazonaws.com/doc/2006-03-01/"><Status>Suspended</Status></VersioningConfiguration>'
        self.assertEqual(s3_bucket("s3_object_bucket_public_read?versioning","put",data = data),200)
    
    def test_028_s3_set_bucket_version(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><VersioningConfiguration xmlns="http://doc.s3.amazonaws.com/doc/2006-03-01/"><Status>Enabled</Status></VersioningConfiguration>'
        self.assertEqual(s3_bucket("s3_object_bucket_public_read?versioning","put",data = data),200)
    
    
    """
    List Buckets
    GET /
    """  
    def test_029_s3_list_bucket(self):
        self.assertEqual(s3_bucket('',"get"),200)
        
    """
    Adds an object to a bucket
    PUT /{bucket}/{object}
    """
    def test_030_s3_create_obj(self):
        for i in range(10):
            header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
            api = "s3_object_bucket_0/test_%s.txt"%i
            self.assertEqual(s3_obj(api,"put",header = header),200)
        
    def test_0301_s3_create_obj(self):
        api = "s3_object_bucket_0/wewe/test_dir.txt"
        self.assertEqual(s3_obj(api,"put"),200)
            
    def test_031_s3_create_obj(self):
        header = {"x-amz-acl": "private",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_4/test_4s.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
            
    def test_032_s3_create_obj(self):
        header = {"x-amz-acl": "private",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_public_read/test_1.html"
        self.assertEqual(s3_obj(api,"put",header = header),200)
            
    def test_033_s3_create_obj(self):
        header = {"x-amz-acl": "authenticated-read",
                  "content-type":"text/html",
                  }
        api = "s3_object_bucket_0/test_10.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
            
    def test_034_s3_create_obj(self):
        header = {"x-amz-acl": "public-read-write",
                  }
        api = "s3_object_bucket_authenticated_read/test_1.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
            
    def test_035_s3_create_obj(self):
        m = hashlib.md5()
        m.update("this is a test!!!")
        header = {"x-amz-acl": "public-read-write",
                  "x-amz-meta-auth":"meto",
                  "content-type":"text/html",
                  "content-md5":base64.b64encode(m.digest()),
                  }
        api = "s3_object_bucket_0/test_11.txt"
        self.assertEqual(s3_obj(api,"put",header = header),400)
    
    def test_036_s3_create_obj(self):
        header = {"x-amz-acl": "public-read-write",
                  "x-amz-meta-auth":"meto",
                  }
        api = "s3_object_bucket_private/test_12.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
            
    def test_037_s3_create_obj(self):
        header = {"x-amz-acl": "private",
                  "x-amz-meta-auth":"meto",
                  }
        api = "s3_object_bucket_authenticated_read/test_13.txt"
        self.assertEqual(s3_obj(api,"put",header = header),200)
        
    """
    Get Bucket Location
    GET /{bucket}?location
    """
    def test_038_s3_location_bucket(self):
        self.assertEqual(s3_bucket("s3_object_bucket_0?location","get"),200)
        
    """
    Get a list of bucket objects
    GET /{bucket}?max-keys=25
    """
    def test_039_s3_list_obj(self):
        self.assertEqual(s3_bucket("s3_object_bucket_0","get"),200)
        
    def test_040_s3_list_objLimit(self):
        self.assertEqual(s3_bucket("s3_object_bucket_0?max-keys=3","get"),200)
        
    def test_041_s3_list_obj(self):
        self.assertEqual(s3_bucket("s3_object_bucket_authenticated_read","get"),200)
        
    def test_042_s3_list_obj(self):
        self.assertEqual(s3_bucket("s3_object_bucket_public_read","get"),200)
        
    def test_043_s3_list_obj(self):
        self.assertEqual(s3_bucket("s3_object_bucket_private","get"),200)
        
    
    """
    Get Bucket ACLs
    GET /{bucket}?acl
    """
    def test_044_s3_get_acl(self):
        self.assertEqual(s3_acl("s3_object_bucket_1?acl","get"),200)
        
    def test_045_s3_get_acl(self):
        info,code = user("uid=rgw_api_1","get",True)
        if code != 200:
            self.assertEqual(code,200)
        else:
            access_key = info["keys"][0]["access_key"]
            secret_key = info["keys"][0]["secret_key"]
            url = "http://%s/%s"%(SERVER,"s3_object_bucket_1?acl")
            r = requests.get(url, auth=S3Auth(access_key, secret_key, SERVER))
            print r.status_code
            self.assertEqual(r.status_code,403)
        
    """
    PUT Bucket ACLs
    PUT /{bucket}?acl
    """
    def test_046_s3_set_acl(self):
        content = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>s3_api</ID><DisplayName>s3_api_ui</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>s3_api</ID><DisplayName>s3_api_ui</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        content = bytearray(content,'utf-8')
        self.assertEqual(s3_acl("s3_object_bucket_1?acl","put",data = content),200)
        
    def test_047_s3_set_acl(self):
        info,code = user("uid=rgw_api_1","get",True)
        if code != 200:
            self.assertEqual(code,200)
        else:
            content = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>s3_api</ID><DisplayName>s3_api_ui</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>s3_api</ID><DisplayName>s3_api_ui</DisplayName></Grantee><Permission>FULL</Permission></Grant></AccessControlList></AccessControlPolicy>'
            content = bytearray(content,'utf-8')
            access_key = info["keys"][0]["access_key"]
            secret_key = info["keys"][0]["secret_key"]
            url = "http://%s/%s"%(SERVER,"s3_object_bucket_1?acl")
            r = requests.put(url, auth=S3Auth(access_key, secret_key, SERVER),data = content)
            print r.status_code
            self.assertEqual(r.status_code,403)
        
        
    """
    Get a list of metadata about all the version of objects within a bucket
    GET /{bucket}?versions
    """
    def test_048_s3_get_version(self):
        self.assertEqual(s3_version("s3_object_bucket_0?versions","get"),200)
    
    def test_049_s3_get_version(self):
        info,code = user("uid=rgw_api_1","get",True)
        if code != 200:
            self.assertEqual(code,200)
        else:
            access_key = info["keys"][0]["access_key"]
            secret_key = info["keys"][0]["secret_key"]
            url = "http://%s/%s"%(SERVER,"s3_object_bucket_0?versions")
            r = requests.get(url, auth=S3Auth(access_key, secret_key, SERVER))
            print "------------------"
            print r.content
            self.assertEqual(r.status_code,200)
            
    def test_050_s3_get_version(self):
        self.assertEqual(s3_version("s3_object_bucket_0?versions&prefix=test","get"),200)
    
    def test_051_s3_get_version(self):
        self.assertEqual(s3_version("s3_object_bucket_0?versions&max-keys=2","get"),200)
    
    
    
    """
    copy an object
    PUT /{dest-bucket}/{dest-object}
    """
    def test_052_s3_copy_obj(self):
        header = {"x-amz-acl":"private"}
        self.assertEqual(s3_obj("s3_object_bucket_2/test.txt","put",header = header,flag =True),200)

    def test_053_s3_copy_obj(self):
        header = {"x-amz-acl":"public-read"}
        self.assertEqual(s3_obj("s3_object_bucket_2/test_2.txt","put",header = header,flag =True),200)
        
    def test_054_s3_copy_obj(self):
        header = {"x-amz-acl":"public-read-write","x-amz-copy-if-none-match":"&quot;dc53e265fbb07bb3c9d9fecc7875eabe&quot;"}
        self.assertEqual(s3_obj("s3_object_bucket_2/test_3.txt","put",header = header,flag =True),200)
        
    def test_055_s3_copy_obj(self):
        header = {"x-amz-acl":"authenticated-read","x-amz-copy-if-match":"&quot;dc53e265fbb07bb3c9d9fecc7875eabe&quot;"}
        code = s3_obj("s3_object_bucket_2/test_4.txt","put",header = header,flag =True)
        if code != 200:
            self.assertEqual(code,412)
        else:
            self.assertEqual(code,200)
    
    
    """
    Get Object
    GET /{bucket}/{object} 
    """
    def test_056_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_2/test.txt","get"),200)
        
    def test_057_s3_get_obj(self):
        r = requests.get("http://%s/s3_object_bucket_0/test_0.txt"%(SERVER))
        print r.content
        self.assertEqual(r.status_code,200)
        
    def test_058_s3_get_obj(self):
        r = requests.get("http://%s/s3_object_bucket_private/test_12.txt"%(SERVER))
        print r.content
        self.assertEqual(r.status_code,200)
        
    def test_059_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_private/test_12.txt","get"),200)
        
    def test_060_s3_get_obj(self):
        
        self.assertEqual(s3_obj("s3_object_bucket_public_read/test_1.html","get"),200)
        
    def test_061_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_authenticated_read/test_1.txt","get"),200)
        
    def test_062_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_authenticated_read/test_1.txt","get"),200)
        
    def test_063_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_4/test_4s.txt","get"),200)
        
    def test_064_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_0/test_10.txt","get"),200)
        
    def test_065_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_0/test_11.txt","get"),404)
    
    """
    Remove Object
    DELETE /{bucket}/{object}
    """
    def test_066_s3_del_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_2/test.txt","delete"),204)
    
    """
    Get Object Information
    HEAD /{bucket}/{object}
    """
    def test_067_s3_head_obInfo(self):
        self.assertEqual(s3_obj("s3_object_bucket_0/test_9.txt","head"),200)
    
    """
    Get Object ACL
    GET /{bucket}/{object}?acl
    """
    def test_068_s3_get_objAcl(self):
        self.assertEqual(s3_obj_acl("s3_object_bucket_0/test_3.txt?acl","get"),200)
    
    """
    Set Object ACL
    PUT /{bucket}/{object}?acl
    """
    def test_069_s3_set_objAcl(self):
        self.assertEqual(s3_obj_acl("s3_object_bucket_0/test_3.txt?acl","put"),200)
        
    """
    multi-part upload
    """
    def test_070_s3_mult_upload(self):
        #self.assertEqual(s3_obj_mult(),200)
        """
        Initiates a multi-part upload process
        POST /{bucket}/{object}?uploads
        """
        header = {"x-amz-acl":"public-read-write","content-type":"text/html"}
        code,info = s3_request("s3_object_bucket_0/disk.img?uploads","post",header = header)
        if code != 200:
            #return code
            self.assertEqual("101",200)
        obj = untangle.parse(info)
        uploadID = obj.InitiateMultipartUploadResult.UploadId.cdata
        
        """
        Adds a part to a multi-part upload.
        PUT /{bucket}/{object}?partNumber=&uploadId={upload-id}
        """
        for i in range(1,4):
            code,info =  s3_request("s3_object_bucket_0/disk.img?partNumber=%s&uploadId=%s"%(i,uploadID),"put")
            if code != 200:
                #return code
                self.assertEqual("102",200)
        """
        Specify the uploadId subresource and the upload ID to list the parts of a multi-part upload.
        GET /{bucket}/{object}?uploadId={upload-id}
        """
        code,info = s3_request("s3_object_bucket_0/disk.img?uploadId=%s"%uploadID,"get")
        if code != 200:
            #return code
            self.assertEqual(103,200)
        info = info.replace("ListPartsResult","CompleteMultipartUpload")
        
        """
        Assembles uploaded parts and creates a new object
        POST /{bucket}/{object}?uploadId= HTTP/1.1
        """
        code,info = s3_request("s3_object_bucket_0/disk.img?uploadId=%s"%uploadID,"post",data = info)
        if code != 200:
            #return code
            self.assertEqual(104,200)
    
        
        """
        get object
        """
        code,info = s3_request("s3_object_bucket_0/disk.img","get")
        if code !=200:
            self.assertEqual(105,200)
    
        """
        ABORT MULTIPART UPLOAD
        DELETE /{bucket}/{object}?uploadId=
        """    
        code,info = s3_request("s3_object_bucket_0/disk.img?uploadId=%s"%uploadID,"delete")
        if code != 404:
            #return code
            self.assertEqual(106,200)
            
        """
        delete
        """
        code,info = s3_request("s3_object_bucket_0/disk.img","delete")
        if code != 204:
            #return code
            self.assertEqual(107,200)
         
    """
    List Bucket Multipart Uploads
    GET /{bucket}?uploads
    """
    def test_071_s3_get_upload(self):
        self.assertEqual(s3_upload("s3_object_bucket_0?uploads","get"),200)
    
    """
    Modify a user.
    POST /admin/user?format=json HTTP/1.1
    @uid
    """
    def test_072_modify_user(self): 
        self.assertEqual(user("uid=rgw_api&email=rgw@163.com","post"),200) 
         
    def test_073_modify_user(self): 
        self.assertEqual(user("uid=rgw_api&display-name=rgw_use","post"),200)
    
    def test_074_modify_user(self): 
        self.assertEqual(user("uid=rgw_api&generate-key=True","post"),200)
        
    def test_075_modify_user(self): 
        self.assertEqual(user("uid=rgw_api_2&access-key=rgw163com&key-type=swift","post"),400)
    
    def test_076_modify_user(self): 
        self.assertEqual(user("uid=rgw_api_2&secret-key=rgw163sdcom","post"),403)
        
    def test_077_modify_user(self): 
        self.assertEqual(user("uid=rgw_api_2&user-caps=buckets=*","post"),200)
        
    def test_078_modify_user(self): 
        self.assertEqual(user("uid=rgw_api&max-buckets=500","post"),200)
        
    def test_079_modify_user(self): 
        self.assertEqual(user("uid=rgw_api&suspended=True","post"),200)
        
    """
    Request bandwidth usage information.\
    GET /admin/usage?format=json HTTP/1.1 \
    @uid
    """
    def test_080_get_usage(self):
        self.assertEqual(usage("show-entries=True&show-summary=True","get"),200)    
     
    def test_081_get_usage(self):
        self.assertEqual(usage("uid=s3_api&start=2016-07-01 00:00:00&show-entries=True&show-summary=True","get"),200)    
     
    def test_082_get_usage(self):
        self.assertEqual(usage("start=2016-07-01 00:00:00&end=2017-07-01 00:00:00&show-entries=True&show-summary=True","get"),200)    
    
    def test_083_get_usage(self):
        self.assertEqual(usage("show-summary=True","get"),200) 
    
    def test_084_get_usage(self):
        self.assertEqual(usage("show-entries=True","get"),200) 
        
    """
    Get user information.
    GET /admin/user?format=json HTTP/1.1
    @uid
    """
    def test_085_get_user(self): 
        self.assertEqual(user("uid=s3_api","get"),200) 
    
    
    """
    Create a new key.
    PUT /admin/user?key&format=json HTTP/1.1
    
    """
    def test_086_create_keys(self):
        self.assertEqual(keys("uid=rgw_api&access-key=abcdefg123456op","put"),200)
        
    def test_087_create_keys_sub(self):
        self.assertEqual(keys("uid=rgw_api_2&subuser=s3_api&access-key=AB01C2D3EF45G6H7IJ8K&key-type=swift","put"),200)
    
    def test_088_create_keys_sub(self):
        self.assertEqual(keys("uid=rgw_api&subuser=s3_api&secret-key=AB01C2D3EF45G6","put"),200)
        
    def test_089_create_keys_sub(self):
        self.assertEqual(keys("uid=rgw_api&generate-key=True","put"),200)
    
    """
    Modify an existing subuser
    POST /admin/user?subuser&format=json HTTP/1.1
    @uid
    @subuser
    """
    def test_090_modify_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&access=full","post"),200)
        
    def test_091_modify_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&generate-secret=True","post"),200)
    
    def test_092_modify_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&secret=qwertyuiop","post"),200)
    
    
    """
    Remove an existing key.
    DELETE /admin/user?key&format=json HTTP/1.1
    @access-key
    """
    def test_093_delete_keys(self):
        self.assertEqual(keys("access-key=abcdefg123456op","delete"),200)
        
    def test_094_delete_keys(self):
        self.assertEqual(keys("access-key=AB01C2D3EF45G6&subuser=s3_api","delete"),403)
        
    def test_095_delete_keys(self):
        self.assertEqual(keys("access-key=AB01C2D3EF45G6H7IJ8K&uid=rgw_api_2","delete"),403)
        self.assertEqual(keys("access-key=AB01C2D3EF45G6H7IJ8K&uid=rgw_api_2&subuser=s3_api","delete"),200)
        
    """
    Get information about a subset of the existing buckets.
    GET /admin/bucket?format=json HTTP/1.1
    
    """
    def test_096_get_buckets(self):
        self.assertEqual(bucket("uid=s3_api&stats=True","get"),200)
        
    def test_097_get_bucket(self):
        self.assertEqual(bucket("bucket=s3_object_bucket_0&stats=True","get"),200)
        
    
    """
    Check the index of an existing bucket
    GET /admin/bucket?index&format=json HTTP/1.1
    @bucket
    """
    def test_098_get_bucket_index(self):
        self.assertEqual(bucket("index&bucket=s3_object_bucket_0","get"),200)
    
    def test_099_get_bucket_index(self):
        self.assertEqual(bucket("index&bucket=s3_object_bucket_0&fix=True","get"),200)
        
    def test_100_get_bucket_index(self):
        self.assertEqual(bucket("index&bucket=s3_object_bucket_0&check-objects=True","get"),200)
    
    """
    Read the policy of an object or bucket.
    GET /admin/bucket?policy&format=json HTTP/1.1
    @bucket
    """
    def test_101_policy_bucket(self):
        self.assertEqual(bucket("policy&bucket=s3_object_bucket_0","get"),200)
    
    def test_102_policy_obj(self):
        self.assertEqual(bucket("policy&bucket=s3_object_bucket_0&object=test_0.txt","get"),200)
        
    
    """
    Add an administrative capability to a specified user.
    PUT /admin/user?caps&format=json HTTP/1.1
    @uid
    @user-caps
    """
    def test_103_add_caps(self):
        self.assertEqual(caps("uid=rgw_api&user-caps=usage=*","put"),200)
    
    """
    Remove an administrative capability from a specified user.
    DELETE /admin/user?caps&format=json HTTP/1.1
    @uid
    @user-caps
    """
    def test_104_delete_caps(self):
        self.assertEqual(caps("uid=rgw_api&user-caps=usage=*","delete"),200)    
    
    """
    Getting User Quota
    GET /admin/user?quota&uid=<uid>&quota-type=user
    @uid
    """
    def test_105_get_user_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=user","get"),200)
        
    """
    Setting User Quota
    PUT /admin/user?quota&uid=<uid>&quota-type=user
    @uid
    """
    def test_106_set_user_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=user","put"),200)
        
    """
    Getting Bucket Quota
    GET /admin/user?quota&uid=<uid>&quota-type=bucket
    @uid
    """
    def test_107_get_bucket_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=bucket","get"),200)
    
    """
    Setting Bucket Quota
    PUT /admin/user?quota&uid=<uid>&quota-type=bucket
    @uid
    """
    def test_108_set_bucket_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=bucket","put"),200)
    
    
    """
    Add the versionId subresource to retrieve a particular version of the object.
    GET /{bucket}/{object}?versionId={versionID} 
    """
    def test_109_s3_get_obj_id(self):
        code = s3_bucket("s3_object_bucket_0/test_0.txt","put")
        if code !=200:
            self.assertEqual("401",200)
        code,info = s3_bucket("s3_object_bucket_0?versions&prefix=test_0","get",ids = True)
        if code != 200:
            self.assertEqual("402",200)
        else:
            obj = untangle.parse(info)
            vid = obj.ListVersionsResult.Version
            self.assertEqual(s3_obj("s3_object_bucket_0/test_0.txt?versionId=%s"%vid[1].VersionId.cdata,"get"),200)
        
    """
    Add the versionId subresource to retrieve info for a particular version.

    HEAD /{bucket}/{object}?versionId={versionID}
    """
    def test_110_s3_head_obInfo_Id(self):
        code,info = s3_bucket("s3_object_bucket_0?versions&prefix=test_0","get",ids = True)
        if code != 200:
            self.assertEqual(code,200)
        else:
            obj = untangle.parse(info)
            vid = obj.ListVersionsResult.Version
            self.assertEqual(s3_obj("s3_object_bucket_0/test_0.txt?versionId=%s"%vid[1].VersionId.cdata,"head"),200)
    
    """
    Add the versionId subresource to retrieve the ACL for a particular version.

    GET /{bucket}/{object}versionId={versionID}&acl 
    """
    def test_111_s3_get_objAcl_Id(self):
        code,info = s3_bucket("s3_object_bucket_0?versions&prefix=test_0","get",ids = True)
        if code != 200:
            self.assertEqual(code,200)
        else:
            obj = untangle.parse(info)
            vid = obj.ListVersionsResult.Version
            self.assertEqual(s3_obj_acl("s3_object_bucket_0/test_0.txt?versionId=%s&acl"%vid[1].VersionId.cdata,"get"),200)
    
    """
    Unlink a bucket from a specified user
    POST /admin/bucket?format=json HTTP/1.1
    @bucket
    @uid
    """
    def test_112_unlink_bucket(self):
        self.assertEqual(bucket("bucket=s3_object_bucket_4&uid=s3_api","post"),200)
    
    """
    Link a bucket to a specified user
    PUT /admin/bucket?format=json HTTP/1.1
    @bucket
    @uid
    """
    def test_113_link_bucket(self):
        content =  bucket("bucket=s3_object_bucket_2&stats=True","get",True)
        if content[0] == 200:
            ids = content[1]["id"]
            self.assertEqual(bucket("uid=s3_api&bucket=s3_object_bucket_2&bucket-id=%s"%ids,"put"),200)
        else:
            self.assertEqual(content[0],200)
            
        self.assertEqual(s3_obj("s3_object_bucket_2/test_2.txt","get"),200)
    
        
    """
    Remove an existing object.
    DELETE /admin/bucket?object&format=json HTTP/1.1
    @bucket
    @object
    """
    def test_114_delete_obj(self):
        self.assertEqual(bucket("object&bucket=s3_object_bucket_0&object=test_4.txt","delete"),200)    
        self.assertEqual(bucket("object&bucket=s3_object_bucket_0&object=test_dir.txt","delete"),200)    
    """
    Deletes a bucket
    DELETE /{bucket}
    """
    def test_115_s3_delete_bucket(self):
        self.assertEqual(s3_bucket("s3_object_bucket_4","delete"),409)
        
    """
    Delete an existing bucket.\
    DELETE /admin/bucket?format=json HTTP/1.1 \
    @bucket
    """
    def test_116_delete_bucke(self):
        for i  in ["s3_object_bucket_4","s3_object_bucket_2","s3_object_bucket_1","s3_object_bucket_3","s3_object_bucket_authenticated_read","s3_object_bucket_private","s3_object_bucket_public_read","s3_object_bucket_0"]:
            self.assertEqual(bucket("bucket=%s&purge-objects=True"%i,"delete"),200)
    
    """
    Remove usage information. With no dates specified, removes all usage information.\
    DELETE /admin/usage?format=json HTTP/1.1 
    """
    def test_117_del_usage(self):
        self.assertEqual(usage("uid=s3_api&start=2016-07-01 00:00:00&end=2016-07-19 10:00:00","delete"),200)
    
    
    def test_118_del_usage(self):
        self.assertEqual(usage("uid=s3_api","delete"),200)
        
    def test_119_del_usage(self):
        self.assertEqual(usage("remove-all=True","delete"),200)
        
    """
    Remove an existing subuser
    DELETE /admin/user?subuser&format=json HTTP/1.1
    @uid
    @subuser
    """
    def test_120_delete_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&purge-keys=True","delete"),200)
    
    """
    Remove an existing user.
    DELETE /admin/user?format=json HTTP/1.1
    @uid
    @purge-data
    """
    
    def test_121_delete_user(self):
        for i in ["rgw_api_1","rgw_api_2","rgw_api_3","rgw_api_4","rgw_api_5","rgw_api_6","rgw_api_7","rgw_api_9","rgw_api","s3_api","Admin_api"]:
            self.assertEqual(user("uid=%s&purge-data=True"%i,"delete"),200)
        
if __name__ == "__main__":
    
   
    hostName = socket.gethostname()
    SERVER = "%s:8000"%hostName
    out =   os.popen("/root/ceph/src/radosgw-admin user create --uid=Admin_api --display_name=api --caps='users=*;usage=*;buckets=*;metadata=*;zone=*'")
    result = out.readlines()[11:14]
    print result
    ADMIN_ACCESS_KEY = result[0].split('"')[3]
    ADMIN_SECRET_KEY = result[1].split('"')[3]
    info = user("uid=s3_api","get",True)
    if info[1] == 404:
        info = user("uid=s3_api&display-name=test","put",True)
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
    
