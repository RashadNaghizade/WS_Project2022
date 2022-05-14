# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider

class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):    
    name = 'link_lists'
    allowed_domains = ['https://myanimelist.net/']
    start_urls = ['https://myanimelist.net/anime.php#/']

    def parse(self, response):

        xpath = '//a[re:test(@class, "genre-name-link")]/@href'
        selection = response.xpath(xpath)
        for s in selection[:18] :
            l = Link()
            l['link'] = 'https://myanimelist.net' + s.get()
            yield l
