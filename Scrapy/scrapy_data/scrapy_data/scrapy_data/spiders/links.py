# -*- coding: utf-8 -*-
import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['https://myanimelist.net/']
    try:
        with open("link_lists.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        print(response)
        xpath = '//a[re:test(@class, "link-image")]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = s.get()
            print(l)
            yield l


