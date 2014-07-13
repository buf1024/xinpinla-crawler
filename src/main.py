#!/usr/bin/env python
#coding: utf-8

import os
import sys
import logging
import setting
import xinpinla
import cache
import kr36
import hexo
import publish
import html2markdown
import datetime
import time

def daemonize(pidfile):
    if os.name == "posix":
        try:
            pid = os.fork()
            if pid > 0:
                sys.stdout.write("Daemon process pid %d" % pid)
                sys.exit(0)
        except OSError, err:
            sys.stderr.write("Fork 1 has failed --> %d--[%s]\n" % (err.errno,
                                                              err.strerror))
            sys.exit(1)

        #os.chdir('/')
        os.setsid()
        os.umask(0)
        
        try:
            pid = os.fork()
            if pid > 0:
                sys.stdout.write("Daemon process pid %d" % pid)
                sys.exit(0)
        except OSError, err:
            sys.stderr.write("Fork 2 has failed --> %d--[%s]\n" % (err.errno,
                                                              err.strerror))
            sys.exit(1)
        
       
        pid = os.getpid()
        try:
            with open(pidfile, "w") as f:
                f.write(str(pid))
        except Exception, e:
            sys.stderr.write("Write pid file failed\n" + str(e))
            sys.exit(1)     
        
        sys.stdout.flush()
        sys.stderr.flush()

def main():
    if setting.daemon:
        daemonize(setting.pid_file)
    
    formatter = logging.Formatter("[%(levelname)s@%(created)s] %(message)s")
    file_handler = logging.FileHandler(setting.log_file)
    file_handler.setFormatter(formatter)
    
    log = logging.getLogger(setting.log_hdr)
    
    log.setLevel(setting.log_level)
    log.addHandler(file_handler)
    
    if setting.log_level == logging.DEBUG:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(formatter)
        log.setLevel(setting.log_level)
        log.addHandler(stdout_handler)

    log.info("logger setting up")

    while True:
        c = cache.Cache()
        t_begin = time.time()
        post = xinpinla.crawler_page(c)
        publish_flag = False
        for k, l in post.items():
            post_time = k
            for d in l:
                title = d["title"]
                link = d["link"]
                desc = d["desc"]
                
                s = kr36.search(title)
                if s == None:
                    n = datetime.datetime.now()
                    n = "%04d-%02d-%02d %02d:%02d:%02d" % (n.year, n.month, n.day, n.hour, n.minute, n.second)
                    s = {"time":n, "title":title, "link":None, "detail":desc}
                
                post_dat = {"pg_time":post_time, "pg_title":title, "pg_link":link, "pg_desc":desc, \
                            "rst_time":s["time"], "rst_title":s["title"], "rst_link":s["link"], "rst_desc":s["detail"]}
                
                log.debug("title: = > " + post_dat["pg_title"])
                
                parse = html2markdown.Html2MarkdownParser()
                parse.feed(post_dat["rst_desc"].strip())
                detail = parse.get_markdown()
                log.info("hexo => " + post_dat["pg_title"])
                publish_flag = hexo.hexo(post_dat)
                if publish_flag == True:
                    log.info("hexo => " + post_dat["pg_title"] + " success")
                    log.debug("append sync: %s=%s" % (k, link))
                    c.append_sync_one(k, link)

        del c
        if publish_flag == True:
            log.info("post_hexo")
            hexo.post_hexo()
            log.info("publish")
            publish.publish()
        
        t_end = time.time()
        
        log.info("it cost %s seconds for one single loop. start = %d, end = %d" % (t_end - t_begin, t_begin, t_end))        
        log.info("going to sleep %d seconds for next loop" % (setting.sleep_time, ))
        time.sleep(setting.sleep_time)

    log.info("done")
    
if __name__ == "__main__":
    sys.exit(main())