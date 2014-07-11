#!/usr/bin/env python
#coding: utf-8

import setting
import logging
import os
    
def hexo(item):    
    log = logging.getLogger(setting.log_hdr)
    title = item["pg_title"]
    invalid = "\\/:*?\"<>|"
    newtitle = ""
    for i in title:
        if i not in invalid:
            newtitle += i
    title = newtitle
    
    tmpl = u"""layout: 
  - post 
title: '{0}' 
date: {1} 
categories: 网摘 
tags: 创意事物 
---

"""
    t = item["pg_time"]
    hdr = tmpl.format(title, t.encode("utf-8"))
    d = t.split(u" ")
    fname = setting.hexo_dir + "//source//_posts//" + d[0] + "-" + title + ".md"
    
    rst_link = item["rst_link"] 
    tail = u""
    if rst_link != None:
        tail = u"  \n\n\n\n原文发表于 [%s](%s)" % (item["rst_title"], item["rst_link"])
    tmp = u"  \n\n更多详情请参考相关网站 [%s](%s)" % (item["pg_title"], item["pg_link"])
    tail = tail + tmp
    tmp = u"  \n\n本站数据以 [新品啦](http://xinpinla.com/) 作为入口点进行爬取! 并自动发布于github pages上。  \n"
    tail = tail + tmp
    
    ret = False
    
    try:
        with open(fname, "w") as f:
            f.write(hdr.encode("utf-8"))
            f.write(item["rst_desc"].encode("utf-8"))
            f.write(tail.encode("utf-8"))
            ret = True
    except Exception, e:
        log.error("hexo failed: " + str(e))
        
    return ret 
    
def post_hexo():
    log = logging.getLogger(setting.log_hdr)
    dir = os.getcwd()
    
    os.chdir(setting.hexo_dir)
    try:
        hexo_cmd = "hexo g"
        os.system(hexo_cmd)
    except Exception, e:
        log.error("post_hexo failed: " + str(e))
    
    os.chdir(dir)