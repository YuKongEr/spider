# -*- coding: utf-8 -*-
import scrapy

from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫的名称
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['moive.douban.com']
    # 入口url
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']/ol[@class='grid_view']/li")
        for movie in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = movie.xpath(".//div[@class='item']/div/em/text()").extract_first()
            douban_item['movie_name'] = movie.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()")\
                .extract_first()
            context = movie.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            context_s = ""
            for i_context in context:
                context_s += "".join(i_context.split())
            douban_item['introduce'] = context_s
            douban_item['star'] = movie\
                .xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()")\
                .extract_first()
            douban_item['evaluate'] = movie\
                .xpath(".//div[@class='info']/div[@class='bd']/div[@class='star']/span[4]/text()")\
                .extract_first()
            douban_item['describe'] = movie \
                .xpath(".//div[@class='info']/div[@class='bd']/p[@class='quote']/span/text()") \
                .extract_first()
            # 提交给管道
            yield douban_item
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse, dont_filter=True)
