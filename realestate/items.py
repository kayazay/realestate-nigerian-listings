# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListItem(scrapy.Item):
    # define the fields for your item here like:
    ref = scrapy.Field()
    url = scrapy.Field()
    page = scrapy.Field() # about listing webpage
    price_ngn = scrapy.Field()
    period =  scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    toilet = scrapy.Field()
    parking = scrapy.Field()
    area_sqm = scrapy.Field() # quantifiable data about listings
    listdate = scrapy.Field()
    listtype = scrapy.Field()
    details = scrapy.Field()
    address = scrapy.Field() # other listing data
    marketer = scrapy.Field()
    contact = scrapy.Field() # marketer information