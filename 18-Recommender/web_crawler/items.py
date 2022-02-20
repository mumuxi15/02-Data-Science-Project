# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class AnimeItem(scrapy.Item):
    anime = scrapy.Field()
    reviews = scrapy.Field()
    themesongs = scrapy.Field()
    description = scrapy.Field()
    img_url = scrapy.Field()
    anime_type = scrapy.Field()
    air_time = scrapy.Field()

class CharacterItem(scrapy.Item):
    character = scrapy.Field()
    anime = scrapy.Field()
    description = scrapy.Field()
    img_url = scrapy.Field()
    
class UserItem(scrapy.Item):
    user = scrapy.Field()
    anime_id = scrapy.Field()
    anime_title = scrapy.Field()
    anime_score = scrapy.Field()
    anime_type = scrapy.Field()
