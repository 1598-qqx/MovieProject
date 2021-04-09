# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieprojectItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    rate = scrapy.Field()
    category = scrapy.Field()
    intro = scrapy.Field()
