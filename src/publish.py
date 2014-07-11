#!/usr/bin/env python
#coding: utf-8

import setting
import os
import logging

def publish():
    log = logging.getLogger(setting.log_hdr)
    dir = os.getcwd()
    
    os.chdir(setting.pages_dir)
    try:
        git_cmd = "git add ./*"
        os.system(git_cmd)
        
        git_cmd = "git commit -m 'auto commit' -a"
        os.system(git_cmd)
        
        git_cmd = "git push"
        print git_cmd
        os.system(git_cmd)
    except Exception, e:
        log.error("publish: " + str(e))
    
    os.chdir(dir)