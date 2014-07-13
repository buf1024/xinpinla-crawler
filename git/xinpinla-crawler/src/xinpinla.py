#!/usr/bin/env python
#coding: utf-8

import urllib
import setting
import re
import cache
import logging
import datetime

def change_time_fmt(date):
    log = logging.getLogger(setting.log_hdr)
    n = datetime.datetime.now()
    m = n.month
    d = n.day
    try:
        s = date.split(u"月")
        m = int(s[0])
        t = s[1].split(u"日")
        d = int(t[0])
    except Exception, e:
        log.error("change_time_fmt failed: " + str(e))
        m = n.month
        d = n.day
    t = "%04d-%02d-%02d 00:00:00" % (n.year, m, d)
    
    return t
    
# d = {"a":[{"a":1, "b":2}...]}    
def crawler_page(cache):
    log = logging.getLogger(setting.log_hdr)
    url = "http://xinpinla.com/"
    
    post = {}

    try:
        content = urllib.urlopen(url).read()
            
        pattern_all = re.compile("<li class=\"date-one\">.*?</i>(.*?)</h2>.*?<ul class=\"product-list\">.*?</ul>.*?</li>", re.M|re.S)
        pattern_items = re.compile("<li class=\"product-one\".*?<h3>.*?<a.*?title=\"(.*?)\">(.*?)</a>.*?<div class=\"product-description\">(.*?)</div>.*?</li>", re.M|re.S)
        pg_items_iter = pattern_all.finditer(content)
        
        for pm_obj in pg_items_iter:
            # 按时间顺序递减，找出增加的即可            
            pg_date = pm_obj.group(1).strip().decode("utf-8")
            pg_date = change_time_fmt(pg_date)
            log.info("clawler, pg_date = %s" % (pg_date,))
            cache_items = cache.get_sync(pg_date)
            break_flag = False
            if cache_items != None:
                break_flag = True
            else:
                cache_items = []
            log.debug("cache: " + str(cache_items))
            post_t = []
            items_iter = pattern_items.finditer(pm_obj.group(0))
            for mobj in items_iter:
                # 由link唯一标示
                link = mobj.group(1).strip().decode("utf-8")
                title = mobj.group(2).strip().decode("utf-8")
                desc = mobj.group(3).strip().decode("utf-8")
                log.debug("link: " + link)
                log.info("clawler, title = %s, link = %s, desc = %s" % (title, link, desc))
                
                if link not in cache_items:
                    post_t.append({"link":link, "title":title, "desc":desc})
                    cache_items.append(link)
            
            post[pg_date] = post_t
            
            if break_flag == True:
                break
    
    except Exception, e:
        log.error("crawler_page failed: " + str(e))
        post = {}
    
    log.info("post size = %d" % (len(post), ))
    return post
        