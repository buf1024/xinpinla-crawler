#!/usr/bin/env python
#coding: utf-8

import logging

log_level = logging.DEBUG
log_file = "/home/nginx/git/xinpinla-crawler/src/crawler-xinpinla.log"
log_hdr = "crawler"

sleep_time = 30*60

daemon = True
pid_file = "/home/nginx/git/xinpinla-crawler/src/crawler.pid"

cache_file = "/home/nginx/git/xinpinla-crawler/src/cache.shelve"

hexo_dir = "/home/nginx/git/xinpinla-crawler/hexo"

pages_dir =  "/home/nginx/git/xinpinla-crawler-ghpages"

