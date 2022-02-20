# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

    
class AnimeItem(scrapy.Item):
    id = scrapy.Field()
    score = scrapy.Field()
    members = scrapy.Field()
    description = scrapy.Field()
    favorites = scrapy.Field()
    