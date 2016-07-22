#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import socket
import unittest
import untangle
import time 
import hashlib
import base64
import requests
from awsauth import S3Auth


ADMIN_ACCESS_KEY = ''
ADMIN_SECRET_KEY = ''

USER_ACCESS_KEY = ''
USER_SECRET_KEY = ''

OTHER_ACCESS_KEY = ''
OTHER_SECRET_KEY = ''

SUB_ONE_ACCESS_KEY = ''
SUB_TWO_ACCESS_KEY = ''
SUB_ONE_SECRET_KEY = ''
SUB_TWO_SECRET_KEY = ''

SUB_THREE_ACCESS_KEY = ''
SUB_THREE_SECRET_KEY = '' 

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

def other(api,method,header={}):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(OTHER_ACCESS_KEY, OTHER_SECRET_KEY, SERVER),headers = header)
    print url,method
    print r.content,r.status_code
    print r.headers
    print "\n"
    return r.status_code

def sub_one(api,method,header={},data = ''):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(SUB_ONE_ACCESS_KEY, SUB_ONE_SECRET_KEY, SERVER),headers = header)
    print url,method
    print r.content,r.status_code
    print r.headers
    print "\n"
    return r.status_code
    
def sub_two(api,method,header={},data = ''):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(SUB_TWO_ACCESS_KEY, SUB_TWO_SECRET_KEY, SERVER),headers = header)
    print url,method
    print r.content,r.status_code
    print r.headers
    print "\n"
    return r.status_code

def sub_three(api,method,header={},data = ''):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(SUB_THREE_ACCESS_KEY, SUB_THREE_SECRET_KEY, SERVER),headers = header)
    print url,method
    print r.content,r.status_code
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


class TesRgwApi(unittest.TestCase):
    
    def test_001_user_create(self):
        #for i in range(2):
        self.assertEqual(user("uid=guest_0&display-name=acces_api_0","put"),200)
            
    ####################subuser############################################
    def test_002_subuser_create(self):
        for i in range(2):
            self.assertEqual(subuser("uid=xinzhi_api&subuser=xinzhi_api_cloud_%s&key-type=s3&access-key=qwertyu%s&generate-secret=True"%(i,i),"put"),403)
                
    def test_003_subuser_creat(self):
        global SUB_ONE_ACCESS_KEY,SUB_TWO_ACCESS_KEY,SUB_ONE_SECRET_KEY,SUB_TWO_SECRET_KEY,SUB_THREE_ACCESS_KEY,SUB_THREE_SECRET_KEY
        
        os.popen("/root/ceph/src/radosgw-admin subuser create --uid=xinzhi_api --subuser=cloud_user_1 --key-type=s3 --access-key=cloud_user_123 --access=full")
        os.popen("/root/ceph/src/radosgw-admin subuser create --uid=xinzhi_api --subuser=cloud_user_4 --key-type=s3 --access-key=cloud_user_456 --access=read")
        os.popen("/root/ceph/src/radosgw-admin subuser create --uid=xinzhi_api --subuser=cloud_user_7 --key-type=s3 --access-key=cloud_user_789 --access=write")
        
        info = user("uid=xinzhi_api","get","True")
        result = info[0]["keys"]
        SUB_ONE_ACCESS_KEY = result[1]["access_key"]
        SUB_ONE_SECRET_KEY = result[1]["secret_key"]
        SUB_TWO_ACCESS_KEY = result[2]["access_key"]
        SUB_TWO_SECRET_KEY = result[2]["secret_key"]
        SUB_THREE_ACCESS_KEY = result[3]["access_key"]
        SUB_THREE_SECRET_KEY = result[3]["secret_key"]
        
        
    
    def test_004_bucket_create(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            if i !="default_access":
                header = {"x-amz-acl":i}
            else:
                header = {}
            self.assertEqual(s3_bucket("%s"%i,"put",header = header),200)
            
    def test_005_subbucket_create(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            if i !="default_access":
                header = {"x-amz-acl":i}
            else:
                header = {}
            self.assertEqual(sub_one("one_%s"%i,"put",header = header),200)
        
    def test_006_subbucket_create(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            if i !="default_access":
                header = {"x-amz-acl":i}
            else:
                header = {}
            self.assertEqual(sub_two("two_%s"%i,"put",header = header),200)
            
    def test_007_subbucket_create(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            if i !="default_access":
                header = {"x-amz-acl":i}
            else:
                header = {}
            self.assertEqual(sub_three("three_%s"%i,"put",header = header),200)
    
    def test_008_obj_add(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                if j !="default_access":
                    header = {"x-amz-acl":j}
                else:
                    header = {}
                self.assertEqual(s3_obj("%s/%s.txt"%(i,j),"put",header = header),200)
    
    def test_009_subobj_add(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                if j !="default_access":
                    header = {"x-amz-acl":j}
                else:
                    header = {}
                self.assertEqual(sub_one("one_%s/%s.txt"%(i,j),"put",header = header),200)
    
    def test_010_subobj_add(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                if j !="default_access":
                    header = {"x-amz-acl":j}
                else:
                    header = {}
                self.assertEqual(sub_two("two_%s/%s.txt"%(i,j),"put",header = header),403)
                
    def test_011_subobj_add(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                if j !="default_access":
                    header = {"x-amz-acl":j}
                else:
                    header = {}
                self.assertEqual(sub_three("three_%s/%s.txt"%(i,j),"put",header = header),200)
                
    
    def test_012_obj_other_add_private(self):
        global OTHER_ACCESS_KEY,OTHER_SECRET_KEY
        info = user("uid=guest_0","get",True)
        OTHER_ACCESS_KEY = info[0]["keys"][0]["access_key"]
        OTHER_SECRET_KEY = info[0]["keys"][0]["secret_key"]
        header = {"x-amz-acl":"public-read"}
        self.assertEqual(other("private/othert_private.txt","put",header = header),403)
        self.assertEqual(other("one_private/othert_private.txt","put",header = header),403)
        self.assertEqual(other("two_private/othert_private.txt","put",header = header),403)
        self.assertEqual(other("three_private/othert_private.txt","put",header = header),403)
    
    def test_013_obj_other_add_publicr(self):
        header = {"x-amz-acl":"private"}
        self.assertEqual(other("public-read/other_pubs.txt","put",header = header),403)
        self.assertEqual(other("one_public-read/othert_pubs.txt","put",header = header),403)
        self.assertEqual(other("two_public-read/othert_pubs.txt","put",header = header),403)
        self.assertEqual(other("three_public-read/othert_pubs.txt","put",header = header),403)
        
    def test_014_obj_other_add_publicrw(self):
        header = {"x-amz-acl":"private"}
        self.assertEqual(other("public-read-write/other_pubrw.txt","put",header = header),200)
        self.assertEqual(other("one_public-read-write/other_pubrw.txt","put",header = header),200)
        self.assertEqual(other("two_public-read-write/other_pubrw.txt","put",header = header),200)
        self.assertEqual(other("three_public-read-write/other_pubrw.txt","put",header = header),200)
    
    def test_015_obj_other_add_auth(self):
        header = {"x-amz-acl":"private"}
        self.assertEqual(other("authenticated-read/other_private.txt","put",header = header),403)
        self.assertEqual(other("one_authenticated-read/other_private.txt","put",header = header),403)
        self.assertEqual(other("two_authenticated-read/other_private.txt","put",header = header),403)
        self.assertEqual(other("three_authenticated-read/other_private.txt","put",header = header),403)   
    
    
    def test_016_obj_other_add_default(self):
        header = {"x-amz-acl":"authenticated-read"}
        self.assertEqual(other("default_access/other_access.txt","put",header = header),403)
        self.assertEqual(other("one_default_access/other_access.txt","put",header = header),403)
        self.assertEqual(other("two_default_access/other_access.txt","put",header = header),403)
        self.assertEqual(other("three_default_access/other_access.txt","put",header = header),403)      
    
    def test_017_bucket_private_list(self):
        self.assertEqual(s3_bucket("private","get"),200)
        self.assertEqual(s3_bucket("one_private","get"),200)
        self.assertEqual(other("private","get"),403)
        self.assertEqual(sub_one("private","get"),200)
        self.assertEqual(s3_bucket("three_private","get"),200)
        self.assertEqual(other("one_private","get"),403)
        self.assertEqual(sub_two("one_private","get"),200)
    
    def test_018_bucket_publicr_list(self):
        self.assertEqual(s3_bucket("public-read","get"),200)
        self.assertEqual(other("public-read","get"),200)
        self.assertEqual(s3_bucket("one_public-read","get"),200)
        self.assertEqual(sub_one("public-read","get"),200)
        self.assertEqual(s3_bucket("three_public-read","get"),200)
        self.assertEqual(other("two_public-read","get"),200)
        self.assertEqual(sub_three("one_public-read","get"),403)
    
    def test_019_bucket_publicrw_list(self):
        self.assertEqual(s3_bucket("public-read-write","get"),200)
        self.assertEqual(other("public-read-write","get"),200)
        self.assertEqual(s3_bucket("one_public-read-write","get"),200)
        self.assertEqual(other("one_public-read-write","get"),200)
        self.assertEqual(sub_one("public-read-write","get"),200)
        self.assertEqual(s3_bucket("three_public-read-write","get"),200)
        
    def test_020_bucket_authen_list(self):
        self.assertEqual(s3_bucket("authenticated-read","get"),200)
        self.assertEqual(other("authenticated-read","get"),200)
        self.assertEqual(sub_one("authenticated-read","get"),200)
        self.assertEqual(other("one_authenticated-read","get"),200)
        self.assertEqual(s3_bucket("two_authenticated-read","get"),200)
        self.assertEqual(s3_bucket("one_authenticated-read","get"),200)
        self.assertEqual(sub_three("one_authenticated-read","get"),403)
        
    def test_021_bucket_list(self):
        self.assertEqual(s3_bucket("default_access","get"),200)
        self.assertEqual(other("default_access","get"),403)
        self.assertEqual(sub_one("default_access","get"),200)
        self.assertEqual(s3_bucket("one_default_access","get"),200)
        self.assertEqual(other("one_default_access","get"),403)
        self.assertEqual(s3_bucket("two_default_access","get"),200)
        self.assertEqual(sub_three("two_default_access","get"),403)
        
    def test_022_obj_get(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                self.assertEqual(s3_obj("%s/%s.txt"%(i,j),"get"),200)
    
    def test_023_subobj_get(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                self.assertEqual(s3_obj("one_%s/%s.txt"%(i,j),"get"),200)
        
    def test_024_subobj_get(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                self.assertEqual(s3_obj("two_%s/%s.txt"%(i,j),"get"),404)
                
    def test_025_subobj_get(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                self.assertEqual(s3_obj("three_%s/%s.txt"%(i,j),"get"),200)
                
    def test_026_subobj_get(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                self.assertEqual(sub_one("%s/%s.txt"%(i,j),"get"),200)
                
    def test_027_subobj_get(self):
        for i in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
            for j in ["private", "public-read", "public-read-write", "authenticated-read","default_access"]:
                self.assertEqual(sub_three("three_%s/%s.txt"%(i,j),"get"),403)
               
                
    def test_028_obj_other_get(self):
        self.assertEqual(other("private/private.txt","get"),403)
        self.assertEqual(other("one_private/private.txt","get"),403)
        
        
    def test_029_obj_other_get(self):
        self.assertEqual(other("three_private/private.txt","get"),403)
        self.assertEqual(other("private/public-read-write.txt","get"),200)
        
    def test_030_obj_other_get(self):
        self.assertEqual(other("public-read/public-read.txt","get"),200)
        self.assertEqual(other("one_public-read/public-read.txt","get"),200)
        
    def test_031_obj_other_get(self):
        self.assertEqual(other("public-read-write/public-read-write.txt","get"),200)
        self.assertEqual(other("one_public-read-write/public-read-write.txt","get"),200)
        
    def test_032_obj_other_get(self):
        self.assertEqual(other("authenticated-read/authenticated-read.txt","get"),200)
        self.assertEqual(other("one_authenticated-read/authenticated-read.txt","get"),200)
        
    def test_033_obj_other_get(self):
        self.assertEqual(other("default_access/default_access.txt","get"),403)
        self.assertEqual(other("one_default_access/default_access.txt","get"),403)
        
    
    def test_034_obj_other_get(self):
        self.assertEqual(other("default_access/other_access.txt","get"),403)
        
    def test_035_obj_other_get(self):
        self.assertEqual(other("public-read/other_pubs.txt","get"),404)
        
    def test_036_obj_other_get(self):
        self.assertEqual(other("public-read-write/default_access.txt","get"),403)
        
    def test_037_obj_other_get(self):
        self.assertEqual(other("public-read/private.txt","get"),403)
    
    def test_038_obj_other_get(self):
        self.assertEqual(other("public-read-write/private.txt","get"),403)
                
    def test_039_get_bucket_acl(self):
        self.assertEqual(s3_acl("private?acl","get"),200)
        
    def test_040_get_obj_acl(self):
        self.assertEqual(s3_acl("private/private.txt?acl","get"),200)
        
    def test_041_get_obj_acl(self):
        self.assertEqual(sub_one("one_private/private.txt?acl","get"),200)
    
    def test_042_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("private?acl","put",data = data),200)
        
    def test_043_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("one_private?acl","put",data = data),200)
        
    def test_044__add_obj(self):
        self.assertEqual(s3_obj("private/kand_SDF.txt","put"),403)
        self.assertEqual(sub_one("one_private/kand_SDF.txt","put"),403)
        self.assertEqual(s3_obj("one_private/kand_SDF_one.txt","put"),403)
        
    def test_045__get_obj(self):
        self.assertEqual(s3_obj("private/private.txt","get"),200)
        self.assertEqual(s3_obj("private/kand_SDF.txt","get"),404)
        self.assertEqual(sub_one("one_private/kand_SDF.txt","get"),404)
        self.assertEqual(s3_obj("one_private/kand_SDF_one.txt","get"),404)
    
    def test_046_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>WRITE</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("private?acl","put",data = data),200)
        
    def test_047__add_obj(self):
        self.assertEqual(s3_obj("private/kand.txt","put"),200)
        
    def test_048__get_obj(self):
        self.assertEqual(s3_obj("private/kand.txt","get"),200)
        
    def test_049_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>WRITE</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(sub_one("one_private?acl","put",data = data),403)
         
    def test_050__add_obj(self):
        self.assertEqual(sub_one("one_private/kand.txt","put"),403)
     
    def test_051__add_obj(self):
        self.assertEqual(s3_obj("one_private/kand_one.txt","put"),403)
        
    def test_052__get_obj(self):
        self.assertEqual(s3_obj("one_private/kand.txt","get"),404)
        
    def test_053__get_obj(self):
        self.assertEqual(s3_obj("one_private/kand_one.txt","get"),404)
    
    def test_054_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>WRITE</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("public-read-write?acl","put",data = data),200)
        
    def test_055_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>WRITE</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(sub_one("one_public-read-write?acl","put",data = data),403)
        
    def test_056__add_obj(self):
        self.assertEqual(other("public-read-write/kand.txt","put"),403)
        self.assertEqual(s3_obj("public-read-write/kand_s3.txt","put"),200)
        self.assertEqual(sub_one("one_public-read-write/kand.txt","put"),200)
        self.assertEqual(s3_obj("one_public-read-write/kand_s3.txt","put"),200)
        self.assertEqual(other("one_public-read-write/kand_other.txt","put"),200)
        
        
    def test_057__get_obj(self):
        self.assertEqual(other("public-read-write/kand.txt","get"),403)
        self.assertEqual(s3_obj("public-read-write/kand_s3.txt","get"),200)
        self.assertEqual(sub_one("one_public-read-write/kand.txt","get"),200)
        self.assertEqual(s3_obj("one_public-read-write/kand_s3.txt","get"),200)
        self.assertEqual(other("one_public-read-write/kand_other.txt","get"),200)
        
    def test_058_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("public-read-write?acl","put",data = data),200)
    
    def test_059_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("one_public-read-write?acl","put",data = data),200)
    
    def test_060__add_obj(self):
        self.assertEqual(other("public-read-write/kand_DS.txt","put"),403)
        self.assertEqual(s3_obj("public-read-write/kand_s3_1.txt","put"),403)
        self.assertEqual(sub_one("one_public-read-write/kand_o.txt","put"),403)
        self.assertEqual(s3_obj("one_public-read-write/kand_s3_2.txt","put"),403)
        self.assertEqual(other("one_public-read-write/kand_other_1.txt","put"),403)
        
    def test_061__get_obj(self):
        self.assertEqual(other("public-read-write/kand.txt","get"),403)
        self.assertEqual(s3_obj("public-read-write/kand_s3_1.txt","get"),404)
        self.assertEqual(sub_one("one_public-read-write/kand_o.txt","get"),404)
        self.assertEqual(s3_obj("one_public-read-write/kand_s3_2.txt","get"),404)
        self.assertEqual(other("one_public-read-write/kand_other_1.txt","get"),403)
    
    def test_062_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>FULL_CONTROL</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("public-read-write?acl","put",data = data),200)
    
    def test_063_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>FULL_CONTROL</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(s3_acl("one_public-read-write?acl","put",data = data),200)
        
    def test_064__add_obj(self):
        self.assertEqual(other("public-read-write/kand_D.txt","put"),403)
        self.assertEqual(s3_obj("public-read-write/kand_s3_1.txt","put"),200)
        self.assertEqual(sub_one("one_public-read-write/kand_o.txt","put"),200)
        self.assertEqual(s3_obj("one_public-read-write/kand_s3_2.txt","put"),200)
        self.assertEqual(other("one_public-read-write/kand_other_1.txt","put"),403)
        
    def test_065__get_obj(self):
        self.assertEqual(other("public-read-write/kand.txt","get"),403)
        self.assertEqual(s3_obj("public-read-write/kand_s3_1.txt","get"),200)
        self.assertEqual(sub_one("one_public-read-write/kand_o.txt","get"),200)
        self.assertEqual(s3_obj("one_public-read-write/kand_s3_2.txt","get"),200)
        self.assertEqual(other("one_public-read-write/kand_other_1.txt","get"),403)
    
    def test_066_acl_bucket(self):
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>xinzhi_api</ID><DisplayName>test</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        self.assertEqual(sub_one("one_private?acl","put",data = data),403)
    
    def test_067_user(self):
        for i  in ["guest_0","xinzhi_api","Admin_api"]:
        #for i  in ["guest_0","Admin_api"]:
            self.assertEqual(user("uid=%s&purge-data=True"%i,"delete"),200)
        
    
    

if __name__ == "__main__":
    hostName = socket.gethostname()
    SERVER = "%s:8000"%hostName
    out =   os.popen("/root/ceph/src/radosgw-admin user create --uid=Admin_api --display_name=api --caps='users=*;usage=*;buckets=*;metadata=*;zone=*'")
    result = out.readlines()[11:14]
    print result
    ADMIN_ACCESS_KEY = result[0].split('"')[3]
    ADMIN_SECRET_KEY = result[1].split('"')[3]
    info = user("uid=xinzhi_api","get",True)
    if info[1] == 404:
        info = user("uid=xinzhi_api&display-name=test","put",True)
        if info[1] != 200:
            sys.exit(1)
        USER_ACCESS_KEY = info[0]["keys"][0]["access_key"]
        USER_SECRET_KEY = info[0]["keys"][0]["secret_key"]
    elif info[1] == 200:
        USER_ACCESS_KEY = info[0]["keys"][0]["access_key"]
        USER_SECRET_KEY = info[0]["keys"][0]["secret_key"]
    else:
        print info
    unittest.main()
