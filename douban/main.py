#!/usr/bin/env python
# encoding: utf-8

"""
@author: yukong
@contact: yukongcode@gmail.com
@file: main.py
@time: 2019-01-14 11:06
@desc:
"""

from scrapy import cmdline
cmdline.execute("scrapy crawl douban_spider".split())