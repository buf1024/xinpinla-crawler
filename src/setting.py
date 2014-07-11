#!/usr/bin/env python
#coding: utf-8

import logging

log_level = logging.DEBUG
log_file = "crawler-xinpinla.log"
log_hdr = "crawler"

sleep_time = 30*60

daemon = True
pid_file = "crawler.pid"

cache_file = "cache.shelve"

hexo_dir = "F:\\private\\git\\xinpinla-crawler\\hexo"

pages_dir =  "F:\\private\\git\\xinpinla-crawler-ghpages"

