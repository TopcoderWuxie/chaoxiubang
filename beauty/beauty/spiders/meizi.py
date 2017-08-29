# -*- coding: utf-8 -*-

import re
import copy
import scrapy
import requests
from beauty.items import BeautyItem

class MeiziSpider(scrapy.Spider):
    name = "meizi"
    allowed_domains = ["ycgkja.com", "1985t.com"]
    start_urls = ['http://www.ycgkja.com/']

    def parse(self, response):
        for data in response.xpath("//div[@class='nav both']/ul/li")[1:]:
            url = data.xpath(".//h2/a/@href").extract_first()
            category = data.xpath(".//h2/a/span/text()").extract_first()
            item = BeautyItem()
            item['category'] = category
            response.meta['item'] = item
            yield scrapy.Request(url, callback= self.parse_category_pages, meta= copy.deepcopy(response.meta), dont_filter= True)

    def parse_category_pages(self, response):
        yield scrapy.Request(response.url, callback= self.parse_category, meta= copy.deepcopy(response.meta), dont_filter= True)
        for data in response.xpath("//div[@class='page both']/ul/li")[1:]:
            relative_url = data.xpath(".//a/@href").extract_first()
            yield scrapy.Request(response.urljoin(relative_url), callback= self.parse_category, meta= copy.deepcopy(response.meta), dont_filter= True)

    def parse_category(self, response):
        for data in response.xpath("//div[@class='imgList']/ul/li"):
            link = data.xpath(".//a/@href").extract_first()
            yield scrapy.Request(link, callback= self.parse_photo, meta= copy.deepcopy(response.meta), dont_filter= True)

    def parse_photo(self, response):
        item = response.meta['item']
        resp = response.xpath("//div[@class='arcTitle']")
        title = resp.xpath(".//h1/a/text()").extract_first()
        update_time =  re.findall(u"[\d-]+", "".join([x.strip() for x in resp.xpath(".//em/text()").extract()]))[0]
        url = response.urljoin(resp.xpath(".//script/@src").extract_first())
        click_amount = re.findall("[\d]+", requests.get(url).text)[0]
        tags = u"|".join(response.xpath("//div[@class='arcOther l']/a/text()").extract())
        content = response.xpath("//div[@class='arcOther l']/pp/text()").extract_first()
        item['title'], item['update_time'], item['click_amount'], item['tags'], item['content'] = title, update_time, click_amount, tags, content

        response.meta['item'] = item
        yield scrapy.Request(response.url, callback= self.parse_photo_pages, meta= copy.deepcopy(response.meta), dont_filter= True)
        datas = response.xpath("//div[@class='wrap']/div[@class='page']/ul/li")
        if len(datas) > 4:
            for data in datas[3:-1]:
                link = data.xpath(".//a/@href").extract_first()
                yield scrapy.Request(response.urljoin(link), callback= self.parse_photo_pages, meta= copy.deepcopy(response.meta), dont_filter= True)

    def parse_photo_pages(self, response):
        item = response.meta['item']
        url = response.xpath("//div[@class='article_left_top_body']/a/img/@src").extract_first()
        item['url'] = url
        yield item