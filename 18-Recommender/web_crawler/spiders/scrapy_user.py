import scrapy
import json
import pickle
from data.items import UserItem

'''
scrapy myanimelist users
'''
class UserSpider(scrapy.Spider):
    name = 'user'
    custom_settings = {
                        "DOWNLOAD_DELAY": 3,
                        "CONCURRENT_REQUESTS_PER_DOMAIN": 5,
                        "HTTPCACHE_ENABLED": True}
#    start_urls = ['https://myanimelist.net/profile/Szywek']
    start_urls = pickle.load(open( "userlst.p", "rb" ))
    
    def parse(self, response):
        href = response.xpath('//a[@class="di-ib fl-l lh10 circle anime completed"]/@href').extract_first()
        yield scrapy.Request(
                        url = href, 
                        callback = self.parse_sub,
                        meta={
                            'url': href,
                            })
                                        
    def parse_sub(self, response):
        item = UserItem()
        item['user'] = response.request.meta['url'].split('/')[-1].rstrip('?status=2')
        watched = response.xpath('//table/@data-items').extract_first()
        watched = json.loads(watched)
        
        anime_title =[]
        anime_score = []
        anime_type = []
        anime_id = []
        
        for mv in watched:
            if mv['anime_media_type_string'] in ['TV','Movie','Music']:
                anime_title.append(mv['anime_title'])
                anime_id.append(mv['anime_id'])
                anime_type.append(mv['anime_media_type_string'])
                anime_score.append(mv['score'])
        if sum(anime_score) > 0:
            item['anime_id'] = anime_id
            item['anime_title'] = anime_title
            item['anime_score'] = anime_score
            item['anime_type'] = anime_type
            yield item
            
