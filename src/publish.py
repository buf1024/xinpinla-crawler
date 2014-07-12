#!/usr/bin/env python
#coding: utf-8

import setting
import os
import logging

def publish():
    log = logging.getLogger(setting.log_hdr)
    log.info("start publish")
    dir = os.getcwd()    
    os.chdir(setting.pages_dir)
    try:
        git_cmd = "git add ./*"
        ret = os.system(git_cmd)
        log.info("execute %s ret %d", (git_cmd, ret))
        
        git_cmd = "git commit -m 'auto commit' -a"
        ret = os.system(git_cmd)
        log.info("execute %s ret %d", (git_cmd, ret))
        
        git_cmd = "git push"
        ret = os.system(git_cmd)
        log.info("execute %s ret %d", (git_cmd, ret))
        
    except Exception, e:
        log.error("publish failed " + str(e))
    
    os.chdir(dir)
    log.info("end publish")