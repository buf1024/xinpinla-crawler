#!/usr/bin/env python
#coding: utf-8

import shelve
import logging
import setting

class Cache(object):
    def __init__(self):
        self.db = None
        self.log = logging.getLogger(setting.log_hdr)
        
    def __del__(self):
        if self.db != None:
            self.db.close()

    def get_page_md5(self):
        md5 = None
        try:
            if self.db == None:
                self.db = shelve.open(setting.cache_file)
            has_key = self.db.has_key("page-md5")
            if has_key == True:
                md5 = self.db["page-md5"]
        except Exception, e:
            self.log.error("get_page_md5 failed: " + str(e))
        
        return md5
    
    def set_page_md5(self, md5):
        ret = True
        try:
            if self.db == None:
                self.db = shelve.open(setting.cache_file)
            self.db["page-md5"] = md5
        except Exception, e:
            self.log.error("set_page_md5 failed: " + str(e))
            ret = False
        
        return ret

    def get_sync(self, key):
        value = None
        try:
            if self.db == None:
                self.db = shelve.open(setting.cache_file)
            has_key = self.db.has_key(key)
            if has_key == True:
                value = self.db[key]
        except Exception, e:
           self.log.error("is_sync failed: " + str(e))
        
        return value

    def append_sync_one(self, key, v):
        value = self.get_sync(key)
        if value == None:
            return self.save_sync_one(key, [v])
        value.append(v)
        return self.save_sync_one(key, value)
    
    def save_sync_one(self, key, value):
        try:
            if self.db == None:
                self.db = shelve.open(setting.cache_file)
            #if self.db.has_key(key):
            #    log.error("duplicate entry: " + key)
            #    return False
            self.db[key] = value
        except Exception, e:
            self.log.error("save_sync_one failed: " + str(e))
            return False
        
        return True
        
    def save_sync(self, kvs):
        try:
            for k, v in kvs.items():
                if self.append_sync_one(k, v) == False:
                    log.error("save_sync failed\n")
                    return False
        except Exception, e:
            self.log.error("save_sync failed: " + str(e))
            return False
        
        return True
                