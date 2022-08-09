# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class ChessDataItem(scrapy.Item):
    url = scrapy.Field()
    init = scrapy.Field()
    name_black = scrapy.Field()
    name_red = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    move_list = scrapy.Field()
    desc = scrapy.Field()
    result = scrapy.Field()