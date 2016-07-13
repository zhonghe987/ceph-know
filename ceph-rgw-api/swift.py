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
import md5
from awsauth import S3Auth
import hmac
from hashlib import sha1


ADMIN_ACCESS_KEY = ''
ADMIN_SECRET_KEY = ''

USER = ''
USER = ''
USER_TOKEN = ''
SERVER = ''

METHOD = {"put":requests.put,"get":requests.get,"post":requests.post,"delete":requests.delete,"head":requests.head}

"""
 rgw enable usage log = true
 rgw usage log tick interval = 30
 rgw usage log flush threshold = 1024
 rgw usage max shards = 32
 rgw usage max user shards = 1
"""
def user(api,method,flag = False):
    url = "http://%s/admin/user?%s&format=json"%(SERVER,api)
    r = METHOD[method](url, auth=S3Auth(ADMIN_ACCESS_KEY, ADMIN_SECRET_KEY, SERVER))
    #print r.content
    #print url,method
    #print "\n"
    if flag:
        return r.json(),r.status_code
    return r.status_code 

def auth(api,method):
    global USER_TOKEN
    headers = {"X-Auth-User":USER,
               "X-Auth-Key":USER_SECRET_KEY,
               }
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url,headers = headers)
    print r.headers
    USER_TOKEN = r.headers["x-auth-token"]
    print USER_TOKEN
    return r.status_code

def contain(api,method,flag = False):
    header = {"X-Auth-Token":USER_TOKEN,
              }
    #if method == "put":
    #    header["X-Container-Read"] = 
    #    header["X-Container-Write"] = {comma-separated-uids}
    #    header["X-Container-Meta-{key}"] = {value}
    #    header["X-Storage-Policy"] = {placement-pools-key}"
    
    if method == "post": 
        if flag:
            header["X-Container-Meta-Color"] =  "red" 
        else:
            header["X-Container-Read"] =  "*" 
    url = "http://%s/%s"%(SERVER,api)
    print url
    r = METHOD[method](url,headers = header)
    print r.content
    return r.status_code

def obj(api,method,flag = False):
    header = {"X-Auth-Token":USER_TOKEN}
    data = ''
    if flag:
        header["X-Copy-From"] =  "register_0/test.txt"
    if method == "post":
        header["X-Object-Meta-Color"] = "Red"
    elif method == "put":
        data = "this is a swift"
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url,headers = header,data = data)
    print r.content
    return r.status_code
    
    
def temUrl(api,method):
    header = {"X-Auth-Token":USER_TOKEN,"X-Account-Meta-Temp-URL-Key":"abcdefg123456789"}
    url = "http://%s/%s"%(SERVER,api)
    r = METHOD[method](url,headers = header)
    print r.content
    return r.status_code

def temObjUrl(api,method):
    duration_in_seconds = 600  # Duration for which the url is valid
    key = 'abcdefg123456789'
    expires = int(time.time() + duration_in_seconds)
    hmac_body = '%s\n%s\n%s' % ("GET", expires, api)
    #hmac_body = hmac.new(key, hmac_body, sha1).hexdigest()
    sig = hmac.new(key, hmac_body, sha1).hexdigest()
    rest_uri = "{host}{path}?temp_url_sig={sig}&temp_url_expires={expires}".format(
    host="http://192.168.189.141:8000/swift", path=api, sig=sig, expires=expires)
    print rest_uri
    r = METHOD[method](rest_uri)
    return r.status_code

class TesRgwApi(unittest.TestCase):
    
    """
    To authenticate a user
    GET /auth HTTP/1.1
    """
    def test_01_auth(self):
        self.assertEqual(auth("auth","get"),204)
        
    """
    Create a Container
    """
    def test_02_create_contain(self):
        for i in range(2):
            self.assertEqual(contain("swift/v1/register_%s"%i,"put"),201)
    
    """
    Create/Update an Object
    """
    def test_03_create_obj(self):
        self.assertEqual(obj("swift/v1/register_0/test.txt","put"),201)
        
    """
    List a Container Objects
    """
    def test_04_list_obj(self):
        self.assertEqual(contain("swift/v1/register_0","get"),200)
    
    """
     Update a Container¡¯s ACLs
    """
    def test_05_acl_contain(self):
        self.assertEqual(contain("swift/v1/register_1","post"),204)
        
    """
    Add/Update Container Metadata
    """
    def test_06_meta_contain(self):
        self.assertEqual(contain("swift/v1/register_0","post",True),204)
        
    """
    Copy an Object
    """
    def test_07_copy_obj(self):
        self.assertEqual(obj("swift/v1/register_1/test.txt","put"),201)
    
    """
    Get an Object
    """
    def test_08_get_obj(self):
        self.assertEqual(obj("swift/v1/register_1/test.txt","get"),200)
    
    """
    Get Object Metadata
    """
    def test_09_get_obj_meta(self):
        self.assertEqual(obj("swift/v1/register_1/test.txt","head"),200)
    
    """
     Add/Update Object Metadata
    """
    def test_10_update_obj_meta(self):
        self.assertEqual(obj("swift/v1/register_1/test.txt","post"),202)
    
    
    """
    POST TEMP-URL KEYS
    """
    def test_11_temurl(self):
        self.assertEqual(temUrl("swift/v1","post"),204)
    
    """
    GET TEM URL
    """
    def test_12_temObj(self):
        self.assertEqual(temObjUrl("/v1/my_names/test.txt","get"),200)

    """
    Delete an Object
    """
    def test_12_del_obj(self):
        for i in range(2):
            self.assertEqual(obj("swift/v1/register_%s/test.txt"%i,"delete"),204)
    
    """
    LIST CONTAINERS
    """
    def test_13_list_contain(self):
        self.assertEqual(contain("swift/v1","get"),200)
    
    """
    Delete a Container
    """
    def test_14_del_contain(self):
        for i in range(2):
            self.assertEqual(contain("swift/v1/register_%s"%i,"delete"),204)
    
        
if __name__ == "__main__":
    
   
    hostName = socket.gethostname()
    SERVER = "%s:8000"%hostName
    out =   os.popen("/root/ceph/src/radosgw-admin user create --uid=Admin_api --display_name=api --caps='users=*;usage=*;buckets=*;metadata=*;zone=*'")
    result = out.readlines()[11:14]
    print result
    ADMIN_ACCESS_KEY = result[0].split('"')[3]
    ADMIN_SECRET_KEY = result[1].split('"')[3]
    info = user("uid=Swift_api","get",True)
    if info[1] == 404:
        user("uid=Swift_api&display-name=swift","put",True)
        info = user("uid=Swift_api&subuser=swift&access=full","put",True)
        if info[1]!=200:
            sys.exit(0)
    elif info[1] == 200:
        swift_access = info[0]["swift_keys"]
        if not swift_access:
            info = user("uid=Swift_api&subuser=swift&access=full","put",True)
            if info[1] != 200:
                sys.exit(1)
    else:
        print info
        sys.exit(2)
    info = user("uid=Swift_api","get",True)
    swift_access = info[0]["swift_keys"]
    USER = swift_access[0]["user"]
    USER_SECRET_KEY = swift_access[0]["secret_key"]
    unittest.main()
