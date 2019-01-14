# -*- coding: utf-8 -*-
import scrapy

from douban.items import PersonItem, GraphicItem, PicItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫的名称
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ["www.nvshens.com"]
    # 入口url
    start_urls = ['https://www.nvshens.com/rank/sum/']

    def parse(self, response):
        # 获取美女列表
        person_list = response.xpath("//div[@class='rankdiv']/div[3]/ul/li/div/div[2]/span[2]/a")
        for i_person in person_list:
           person = PersonItem()
           person['name'] = i_person.xpath(".//font/text()").extract_first()
           person['imgUrl'] = i_person.xpath(".//@href").extract_first()
           # 今天美女详情页面 获取写真列表
           yield scrapy.Request("https://www.nvshens.com" +  person['imgUrl'], callback=self.process_graphic)

        # 获取下一页链接
        next_link = response.xpath("//div[@class='pagesYY']/div/a[last()]/@href").extract()
        # 判断是否还有下一页
        if next_link:
            next_link = next_link[0]
            # 继续请求下一页
            yield scrapy.Request("https://www.nvshens.com/rank/sum/" + next_link, callback = self.parse)

    def process_graphic(self, response):
        # 判断是否 有更多选项
        is_more = response.xpath("//span[@class='archive_more']/a/@href").extract()
        if is_more:
            is_more = is_more[0]
            # 请求进入所有写真专集列表
            yield scrapy.Request("https://www.nvshens.com" + is_more, callback = self.process_graphic_list, )
        else:
            graphic_list = response.xpath("//div[@class='post_entry']/ul[@class='photo_ul']/li")
            for i_graphic in graphic_list:
                graphiic = GraphicItem()
                graphiic['name'] = i_graphic.xpath(".//div[@class='igalleryli_title']/a/text()").extract_first()
                graphiic['imgUrl'] = i_graphic.xpath(".//div[@class='igalleryli_title']/a/@href").extract_first()
                yield scrapy.Request("https://www.nvshens.com" +  graphiic['imgUrl'], callback=self.process_img, )

    def process_graphic_list(self, response):
        graphic_list = response.xpath("//div[@class='post_entry']/div/ul[@class='photo_ul']/li")
        for i_graphic in graphic_list:
            graphiic = GraphicItem()
            graphiic['name'] = i_graphic.xpath(".//div[@class='igalleryli_title']/a/text()").extract_first()
            graphiic['imgUrl'] = i_graphic.xpath(".//div[@class='igalleryli_title']/a/@href").extract_first()
            yield scrapy.Request("https://www.nvshens.com" + graphiic['imgUrl'], callback=self.process_img, )

    def process_img(self, response):
        img_list = response.xpath("//div[@class='photos']/div[@class='gallery_wrapper']/ul/img")
        for i_img in img_list:
            pic = PicItem()
            title = response.xpath("//div[@class='albumTitle']/h1/text()").extract_first()
            pic['name'] = i_img.xpath(".//@alt").extract_first()
            pic['imgUrl'] = i_img.xpath(".//@src").extract_first()
            pic['title'] = title
            yield pic
        # 获取下一页链接
        next_link = response.xpath("//div[@id='pages']/a[last()]/@href").extract()
        # 判断是否还有下一页
        if next_link:
            next_link = next_link[0]
            # 继续请求下一页
            yield scrapy.Request("https://www.nvshens.com" + next_link, callback=self.process_img, )