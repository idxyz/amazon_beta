# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonBetaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    updated_time = scrapy.Field()
    # sku = scrapy.Field()
    # asin = scrapy.Field()
    # review_link = scrapy.Field()
    # review_date = scrapy.Field()
    star = scrapy.Field()
    author = scrapy.Field()
    pub_date = scrapy.Field()
    isVP = scrapy.Field()
    href = scrapy.Field()
    customerId = scrapy.Field()
    author_href = scrapy.Field()
    asin = scrapy.Field()
    # facebook, twitter, pinterest, instagram, youtube
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    pinterest = scrapy.Field()
    instagram = scrapy.Field()
    youtube = scrapy.Field()
    # isVP = scrapy.Field()
    # profileID = scrapy.Field()
