#!/usr/bin/env python
#coding: utf-8

import urllib
import setting
import re
import cache
import logging

def fetch_detail(url):
    log = logging.getLogger(setting.log_hdr)
    ret = None
    try:
        content = urllib.urlopen(url).read()
        pattern = re.compile("<section class=\"article\">(.*?)</section>", re.M|re.S)
        mobj = pattern.search(content)
        if mobj == None:
            log.warn("not fetch_detail result for " + url)
            return None
        ret = mobj.group(1).strip().decode("utf-8")
    except Exception, e:
        log.error("fetch_detail failed: " + str(e))
    
    return ret
        
def change_time_format(time):
    l = time.split("-")
    date = l[0]
    time = l[1]
    
    d = date.split("/")
    d = "-".join(d)
    
    return d + " " + time + ":00"
    
# {"time":time, "title":title, "link":link, "detail":detail}    
def search(keyword):
    const_url = u"http://www.36kr.com/search/?q="
    log = logging.getLogger(setting.log_hdr)
    
    keyword = keyword.split(u" ")
    keyword = u"+".join(keyword)
    url = const_url + urllib.quote(keyword.encode("utf-8"))
    
    ret = None
    
    try:
        content = urllib.urlopen(url).read()
        pattern = re.compile("<table class=\"table\">.*?<tr>.*?<td>(.*?)</td>.*?<td><a href=\"(.*?)\".*?>(.*?)</a></td>.*?</table>", re.M|re.S)
        
        #如果有多个结果，取第一个
        mobj = pattern.search(content)
        if mobj == None:
            log.warn("no search result for " + keyword)
            return None
        
        time = mobj.group(1).strip().decode("utf-8")
        link = mobj.group(2).strip().decode("utf-8")
        title = mobj.group(3).strip().decode("utf-8")
        
        time = change_time_format(time)
        
        log.info("crawler, time=%s, link=%s, title=%s" % (time, link, title))
        
        const_detail_url = u"http://www.36kr.com"
        url = const_detail_url + link
        detail = fetch_detail(url)
        
        ret = {"time":time, "title":title, "link":url, "detail":detail}
        
    except Exception, e:
        log.error("search failed: " + str(e))
        
    return ret    