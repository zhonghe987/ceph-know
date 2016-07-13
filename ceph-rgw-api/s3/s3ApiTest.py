#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

#easy_install requests-aws
#easy_install requests
#easy_install untangle

import sys

import unittest
import requests
import untangle
import time 
import md5
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
    print r.content
   
    print url,method
    print "\n"
    return r.status_code 

def user(api,method,flag = False):
    url = "http://%s/admin/user?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print r.content
    
    print url,method
    print "\n"
    if flag:
        return r.json(),r.status_code
    return r.status_code 

def subuser(api,method):
    url = "http://%s/admin/user?subuser&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print r.content
    
    print url,method
    print "\n"
    return r.status_code 

def keys(api,method):
    url = "http://%s/admin/user?key&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print r.content
    
    print url,method
    print "\n"
    return r.status_code 

def bucket(api,method):
    url = "http://%s/admin/bucket?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print r.content
    
    print url,method
    print "\n"
    return r.status_code

def caps(api,method):
    url = "http://%s/admin/user?caps&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    print r.content
    
    print url,method
    print "\n"
    return r.status_code

def quota(api,method):
    contents = ''
    if method == 'put':
        contents = bytearray('{"enabled":true,"max_size_kb":1000000,"max_objects":100}','utf-8') 
    url = "http://%s/admin/user?quota&%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER),data = contents)
    print r.content
    
    print url,method
    print "\n"
    return r.status_code
    
    
def s3_bucket(api,method):
    header = {}
    if method == "put":
        header = {"x-amz-acl": "public-read-write"}
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header)
    print r.content
    print url,method
    print "\n"
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

def s3_acl(api,method):
    content = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>testid</ID><DisplayName>testid_ui</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>testid</ID><DisplayName>testid_ui</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
    content = bytearray(content,'utf-8')
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),data = content)
    print r.content
    print url,method   
    print "\n"
   
    return r.status_code

def s3_upload(api,method):
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER))
    print r.content
    
    print url,method
    print "\n"
    return r.status_code


def s3_obj(api,method,flag = False): 
    header,data = {},''
    url = "http://%s/%s"%(SERVER,api)
    if method == "put":
        header = {"x-amz-acl": "public-read-write",
                  "content-type":"text/html",
                  }
        data = "this is a test!!!"
        if flag:
            header["x-amz-copy-source"] =  "s3_object_bucket_0/test_2.txt" 
            r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header)
            return r.status_code
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = data)
    print r.content
    
    print url,method
    print "\n"
    return r.status_code

def s3_obj_acl(api,method):
    header,data = {},''
    if method == "put":
        #header = {"x-amz-acl": "private"}
        data = '<?xml version="1.0" encoding="UTF-8"?><AccessControlPolicy xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>testid</ID><DisplayName>testid_ui</DisplayName></Owner><AccessControlList><Grant><Grantee xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="CanonicalUser"><ID>testid</ID><DisplayName>testid_ui</DisplayName></Grantee><Permission>READ</Permission></Grant></AccessControlList></AccessControlPolicy>'
        
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),headers = header,data = data)
    print r.content
    
    print url,method
    print "\n"
    
    return r.status_code

def s3_request(api,method):
    url = "http://%s/%s"%(SERVER,api)
    if method == "put":
        data = "this is a test"
        r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER),data = data)
    else:
        r = METHOD[method](url, auth=S3Auth(USER_ACCESS_KEY, USER_SECRET_KEY, SERVER))

    
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
    code,info = s3_request("s3_object_bucket_0/disk.img?uploadId=%s"%uploadID,"get")
    if code != 200:
        return code
    return code


class TesRgwApi(unittest.TestCase):
    
    """
    Create a new user.
    PUT /admin/user?format=json HTTP/1.1
    @uid
    @display-name
    """
    def test_01_create_user(self): 
        self.assertEqual(user("uid=rgw_api&display-name=api","put"),200) 
        
    """
    Create a new subuser 
    PUT /admin/user?subuser&format=json HTTP/1.1
    @uid
    @subuser 
    @gen-subuser
    """
    def test_02_create_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&access=read","put"),200)
    
    """
    Creates a new bucket.
    PUT /{bucket}
    """
    def test_03_s3_create_bucket(self):
        for i  in range(5):
            self.assertEqual(s3_bucket('s3_object_bucket_%s'%i,"put"),200)
            
    """
    List Buckets
    GET /
    """  
    def test_04_s3_list_bucket(self):
        self.assertEqual(s3_bucket('',"get"),200)
        
    """
    Adds an object to a bucket
    PUT /{bucket}/{object}
    """
    def test_05_s3_create_obj(self):
        for i in range(10):
            api = "s3_object_bucket_0/test_%s.txt"%i
            self.assertEqual(s3_obj(api,"put"),200)
    
    """
    Get Bucket Location
    GET /{bucket}?location
    """
    def test_06_s3_location_bucket(self):
        self.assertEqual(s3_bucket("s3_object_bucket_0?location","get"),200)
        
    """
    Get a list of bucket objects
    GET /{bucket}?max-keys=25
    """
    def test_07_s3_list_obj(self):
        self.assertEqual(s3_bucket("s3_object_bucket_0","get"),200)
        
    def test_08_s3_list_objLimit(self):
        self.assertEqual(s3_bucket("s3_object_bucket_0?max-keys=3","get"),200)
    
    """
    Get Bucket ACLs
    GET /{bucket}?acl
    """
    def test_09_s3_get_acl(self):
        self.assertEqual(s3_acl("s3_object_bucket_1?acl","get"),200)
        
    """
    PUT Bucket ACLs
    PUT /{bucket}?acl
    """
    def test_10_s3_set_acl(self):
        self.assertEqual(s3_acl("s3_object_bucket_1?acl","get"),200)
        
        
    """
    Get a list of metadata about all the version of objects within a bucket
    GET /{bucket}?versions
    """
    def test_11_s3_get_version(self):
        self.assertEqual(s3_version("s3_object_bucket_0?versions","get"),200)
    
    """
    copy an object
    PUT /{dest-bucket}/{dest-object}
    """
    def test_12_s3_copy_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_2/test.txt","put",True),200)
    
    """
    Get Object
    GET /{bucket}/{object} 
    """
    def test_13_s3_get_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_2/test.txt","get"),200)
    
    """
    Remove Object
    DELETE /{bucket}/{object}
    """
    def test_14_s3_del_obj(self):
        self.assertEqual(s3_obj("s3_object_bucket_2/test.txt","delete"),204)
    
    """
    Get Object Information
    HEAD /{bucket}/{object}
    """
    def test_15_s3_head_obInfo(self):
        self.assertEqual(s3_obj("s3_object_bucket_0/test_9.txt","head"),200)
    
    """
    Get Object ACL
    GET /{bucket}/{object}?acl
    """
    def test_16_s3_get_objAcl(self):
        self.assertEqual(s3_obj_acl("s3_object_bucket_0/test_3.txt?acl","get"),200)
    
    """
    Set Object ACL
    PUT /{bucket}/{object}?acl
    """
    def test_17_s3_set_objAcl(self):
        self.assertEqual(s3_obj_acl("s3_object_bucket_0/test_3.txt?acl","put"),200)
        
    """
    multi-part upload
    """
    def test_18_s3_mult_upload(self):
        self.assertEqual(s3_obj_mult(),200)
         
    """
    List Bucket Multipart Uploads
    GET /{bucket}?uploads
    """
    def test_19_s3_get_upload(self):
        self.assertEqual(s3_upload("s3_object_bucket_0?uploads","get"),200)
    
    """
    Modify a user.
    POST /admin/user?format=json HTTP/1.1
    @uid
    """
    def test_20_modify_user(self): 
        self.assertEqual(user("uid=rgw_api&email=rgw@163.com","post"),200)  
        
    """
    Request bandwidth usage information.\
    GET /admin/usage?format=json HTTP/1.1 \
    @uid
    """
    def test_21_get_usage(self):
        self.assertEqual(usage("uid=testid&start=2016-07-01 00:00:00&show-entries=True&show-summary=True","get"),200)    
    
    """
    Get user information.
    GET /admin/user?format=json HTTP/1.1
    @uid
    """
    def test_22_get_user(self): 
        self.assertEqual(user("uid=testid","get"),200) 
    
    
    """
    Create a new key.
    PUT /admin/user?key&format=json HTTP/1.1
    
    """
    def test_23_create_keys(self):
        self.assertEqual(keys("uid=rgw_api&access-key=abcdefg123456op","put"),200)
        
    def test_24_create_keys_sub(self):
        self.assertEqual(keys("uid=rgw_api&subuser=s3_api&access-key=AB01C2D3EF45G6H7IJ8K","put"),200)
    
    
    """
    Modify an existing subuser
    POST /admin/user?subuser&format=json HTTP/1.1
    @uid
    @subuser
    """
    def test_25_modify_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&access=full","post"),200)
    
    """
    Remove an existing key.
    DELETE /admin/user?key&format=json HTTP/1.1
    @access-key
    """
    def test_26_delete_keys(self):
        self.assertEqual(keys("access-key=abcdefg123456op","delete"),200)
       
    
    """
    Get information about a subset of the existing buckets.
    GET /admin/bucket?format=json HTTP/1.1
    
    """
    def test_27_get_buckets(self):
        self.assertEqual(bucket("uid=testid&stats=True","get"),200)
        
    def test_28_get_bucket(self):
        self.assertEqual(bucket("bucket=s3_object_bucket_0&stats=True","get"),200)
    
    """
    Check the index of an existing bucket
    GET /admin/bucket?index&format=json HTTP/1.1
    @bucket
    """
    def test_29_get_bucket_index(self):
        self.assertEqual(bucket("index&bucket=s3_object_bucket_0","get"),200)
    
    """
    Read the policy of an object or bucket.
    GET /admin/bucket?policy&format=json HTTP/1.1
    @bucket
    """
    def test_30_policy_bucket(self):
        self.assertEqual(bucket("policy&bucket=s3_object_bucket_0","get"),200)
    
    def test_31_policy_obj(self):
        self.assertEqual(bucket("policy&bucket=s3_object_bucket_0&object=test_0.txt","get"),200)
        
    
    """
    Add an administrative capability to a specified user.
    PUT /admin/user?caps&format=json HTTP/1.1
    @uid
    @user-caps
    """
    def test_32_add_caps(self):
        self.assertEqual(caps("uid=rgw_api&user-caps=usage=*","put"),200)
    
    """
    Remove an administrative capability from a specified user.
    DELETE /admin/user?caps&format=json HTTP/1.1
    @uid
    @user-caps
    """
    def test_33_delete_caps(self):
        self.assertEqual(caps("uid=rgw_api&user-caps=usage=*","delete"),200)    
    
    """
    Getting User Quota
    GET /admin/user?quota&uid=<uid>&quota-type=user
    @uid
    """
    def test_34_get_user_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=user","get"),200)
        
    """
    Setting User Quota
    PUT /admin/user?quota&uid=<uid>&quota-type=user
    @uid
    """
    def test_35_set_user_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=user","put"),200)
        
    """
    Getting Bucket Quota
    GET /admin/user?quota&uid=<uid>&quota-type=bucket
    @uid
    """
    def test_36_get_bucket_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=bucket","get"),200)
    
    """
    Setting Bucket Quota
    PUT /admin/user?quota&uid=<uid>&quota-type=bucket
    @uid
    """
    def test_37_set_bucket_quota(self):
        self.assertEqual(quota("uid=rgw_api&quota-type=bucket","put"),200)
    
    
    """
    Add the versionId subresource to retrieve a particular version of the object.
    GET /{bucket}/{object}?versionId={versionID} 
    """
    def test_38_s3_get_obj_id(self):
        self.assertEqual(s3_obj("s3_object_bucket_0/test_0.txt?versionId=2","get"),200)
        
    """
    Add the versionId subresource to retrieve info for a particular version.

    HEAD /{bucket}/{object}?versionId={versionID}
    """
    def test_39_s3_head_obInfo_Id(self):
        self.assertEqual(s3_obj("s3_object_bucket_0/test_0.txt?versionId=2","head"),200)
    
    """
    Add the versionId subresource to retrieve the ACL for a particular version.

    GET /{bucket}/{object}versionId={versionID}&acl 
    """
    def test_40_s3_get_objAcl_Id(self):
        self.assertEqual(s3_obj_acl("s3_object_bucket_0/test_0.txtversionId=2?acl","get"),200)
    
    """
    Unlink a bucket from a specified user
    POST /admin/bucket?format=json HTTP/1.1
    @bucket
    @uid
    """
    def test_41_unlink_bucket(self):
        self.assertEqual(bucket("bucket=s3_object_bucket_4&uid=testid","post"),200)
    
    
    """
    Link a bucket to a specified user
    PUT /admin/bucket?format=json HTTP/1.1
    @bucket
    @uid
    """
    def test_42_link_bucket(self):
        self.assertEqual(bucket("uid=rgw_api&bucket=s3_object_bucket_4","put"),200)
        
    """
    Remove an existing object.
    DELETE /admin/bucket?object&format=json HTTP/1.1
    @bucket
    @object
    """
    def test_43_delete_obj(self):
        self.assertEqual(bucket("object&bucket=s3_object_bucket_0&object=test_4.txt","delete"),200)    
    
    """
    Deletes a bucket
    DELETE /{bucket}
    """
    def test_44_s3_delete_bucket(self):
        self.assertEqual(s3_bucket("s3_object_bucket_3","delete"),204)
        
    """
    Delete an existing bucket.\
    DELETE /admin/bucket?format=json HTTP/1.1 \
    @bucket
    """
    def test_45_delete_bucke(self):
        self.assertEqual(bucket("bucket=s3_object_bucket_0&purge-objects=True","delete"),200)
    
    """
    Remove usage information. With no dates specified, removes all usage information.\
    DELETE /admin/usage?format=json HTTP/1.1 
    """
    def test_46_del_usage(self):
        self.assertEqual(usage("uid=testid","delete"),200)
        
    """
    Remove an existing subuser
    DELETE /admin/user?subuser&format=json HTTP/1.1
    @uid
    @subuser
    """
    def test_47_delete_subuser(self):
        self.assertEqual(subuser("uid=rgw_api&subuser=s3_api&purge-keys=True","delete"),200)
    
    """
    Remove an existing user.
    DELETE /admin/user?format=json HTTP/1.1
    @uid
    @purge-data
    """
    def test_48_delete_user(self):
        self.assertEqual(user("uid=rgw_api&purge-data=True","delete"),200)
        
if __name__ == "__main__":
    #if len(sys.argv) < 4:
    #    sys.exit(0)
    
    #SERVER = sys.argv[1]
    #ADMIN_ACCESS_KEY = sys.argv[2]
    #ADMIN_SECRET_KEY = sys.argv[3]
    SERVER = "objStor02:7480"
    ADMIN_ACCESS_KEY = "8LQDU10IF59POC91P07A"
    ADMIN_SECRET_KEY = "yjfdVcg1UHPO3M2EoBMoCYhpp3sR2ii615jWk79G"
    info = user("uid=testid","get",True)
    if info[1] == 404:
        info = user("uid=testid&display-name=test","put",True)
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
    
    

    
    
    