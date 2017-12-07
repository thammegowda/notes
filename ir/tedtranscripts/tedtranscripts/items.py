# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TedTranscript(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    url = Field()
    lang = Field()
    data = Field()
