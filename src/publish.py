#!/usr/bin/env python
#coding: utf-8

import setting
import os
import logging
import subprocess

def publish():
    log = logging.getLogger(setting.log_hdr)
    log.info("start publish")
    dir = os.getcwd()    
    os.chdir(setting.pages_dir)
    try:
        log.info("auto dir = " + os.getcwd())
        
        git_cmd = ["git", "add", "./*"]
        ret = subprocess.call(git_cmd)
        log.info("execute \"%s\" ret %d" % (str(git_cmd), ret))
        
        git_cmd = ["git", "commit", "-m", "'auto commit'", "-a"]
        ret = subprocess.call(git_cmd)
        log.info("execute \"%s\" ret %d" % (str(git_cmd), ret))
        
        git_cmd = ["git", "push"]
        ret = subprocess.call(git_cmd)
        log.info("execute \"%s\" ret %d" % (str(git_cmd), ret))
        
    except Exception, e:
        log.error("publish failed " + str(e))
    
    os.chdir(dir)
    log.info("end publish")