# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

from douban.items import PersonItem, GraphicItem, PicItem


class DoubanPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        yield Request(item['imgUrl'],meta={'name':item['name'],'title':item['title']})

    def file_path(self, request, response=None, info=None):
        title = request.meta['title']
        name = request.meta['name']
        title = re.sub(r'[？\\*|“<>:/()]', '', title)
        name = re.sub(r'[？\\*|“<>:/()]', '', name)
        ext = request.url.split('/')[-1].split(".")[1]
        filename = u'sexygirl/{0}/{1}'.format(title, name + "." + ext)
        return filename

