# -*- coding: utf-8 -*-
import scrapy

class Animes(scrapy.Item):
    name        = scrapy.Field()
    score       = scrapy.Field()
    rank       = scrapy.Field()
    popularity = scrapy.Field()
    members = scrapy.Field()
    date = scrapy.Field()
    channel = scrapy.Field()


class LinksSpider(scrapy.Spider):
    name = 'anime'
    allowed_domains = ['https://myanimelist.net/']
    try:
        with open("links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:][:667]
    except:
        start_urls = []

    def parse(self, response):
        p = Animes()

        name_xpath = '//*[@id="contentWrapper"]/div[1]/div/div[1]/div/h1/strong/text()'
        score_xpath = '//span[re:test(@itemprop, "ratingValue")]/text()' 
        rank_xpath = '//span[text()="Ranked "]/strong/text()'
        popularity_xpath = '//span[text()="Popularity "]/strong/text()'
        members_xpath = '//span[text()="Members "]/strong/text()'
        date_xpath = '//span[re:test(@class, "information season")]/a/text()'
        channel_xpath = '//span[re:test(@class, "information type")]/a/text()'
    
        p['name']  = response.xpath(name_xpath).getall()
        p['score'] = response.xpath(score_xpath).getall()
        p['rank'] = response.xpath(rank_xpath).getall()
        p['popularity'] = response.xpath(popularity_xpath).getall()
        p['members'] = response.xpath(members_xpath).getall()
        p['date'] = response.xpath(date_xpath).getall()
        p['channel'] = response.xpath(channel_xpath).getall()

        yield p
