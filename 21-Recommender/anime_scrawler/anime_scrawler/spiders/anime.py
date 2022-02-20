import scrapy
import pandas as pd
from anime_scrawler.items import AnimeItem


"""
cd anime_scrawler
scrapy genspider anime example.com  # create project
scrapy crawl #print to console
scrapy crawl anime -o output.json   # output to json file
"""
class AnimeSpider(scrapy.Spider):
    name = 'anime'
    
    
    def start_requests(self):
        dom = 'https://myanimelist.net/anime/'
        id_list = pd.read_csv('../kaggle_data/anime.csv')['anime_id'].to_list()
        
        for i in id_list[0:2]:
            print (dom+str(i))
            yield scrapy.Request(url=dom+str(i),callback=self.parse)

    def parse(self, response):
        item = AnimeItem()
        
        description = ''.join(response.css('p[itemprop=description]::text').extract()[:-1])
        item['score']= response.css('div[data-id=info1] span::text').extract()[1]
        item['id'] = response.url.split('/')[-2]
        
        numeric = response.css('td.borderClass div.spaceit_pad::text').re(r'\d.*')
        
        item['members'] = numeric[-2]
        item['favorites'] = numeric[-1]
        item['description'] = description
        yield item

#       
#       info_tag = response.css('div.spaceit_pad a::attr(href)').extract()
#       info_bar = response.css('div.spaceit_pad a::text').extract()
#
#       for idx,text in enumerate(info_tag):
#           if 'type' in text:
#               item['type']=info_bar[idx]
#           elif 'producer' in text:
#               item['producer']+=info_bar[idx].split('/')[2] #producter id
#           elif 'genre' in text:
#               item['genre']+=[info_bar[idx].split('/')[-1]]
                
        