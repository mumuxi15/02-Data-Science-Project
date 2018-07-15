import scrapy, re
from data.items import AnimeItem
'''
scrapy animes
scrapy shell 'url'
scrapy crawl character -o some.json
'''

class AnimeSpider(scrapy.Spider):
    name = 'anime'
    custom_settings = {
                        "DOWNLOAD_DELAY": 3,
                        "CONCURRENT_REQUESTS_PER_DOMAIN": 5,
                        "HTTPCACHE_ENABLED": True}
    web = 'https://myanimelist.net/topanime.php'
    start_urls = [web]
    for page in range(50,5000,50):
        start_urls.append(web+f'?limit={page}')

    def text_processing(self,txt):
        txt = [re.sub('[\r\t\n]','',t).replace('_',' ').replace('  ','') for t in txt]
        txt = ''.join(list(filter(None,txt)))
        return txt
        
    def parse(self, response):  
        anime_urls = response.xpath('//a[@class="hoverinfo_trigger fl-l fs14 fw-b"]/@href').extract()
        for href in anime_urls:
            yield scrapy.Request(
                            url = href, 
                            callback = self.parse_sub,
                            meta={
                                'url': href })
                
#    click the link go to detail page               
    def parse_sub(self, response):
        item = AnimeItem()
        description = response.xpath('//span[@itemprop="description"]/text()').extract()
        reviews = response.xpath('//div[@class="spaceit textReadability word-break pt8 mt8"]/node()/text()').extract()
        item['themesongs']  = response.xpath('//span[@class="theme-song"]/text()').extract()
        item['anime_type'] = response.xpath('//span[@class="information type"]/a/text()').extract_first()
        item['img_url'] = response.xpath('//div[@style="text-align: center;"]/a/img/@src').extract_first()
        item['air_time'] = response.xpath('//span[@class="information season"]/a/text()').extract_first()
        item['anime'] = response.xpath('//td[@class="borderClass"]/a/text()').extract_first()  
        item['description'] = self.text_processing(description)
        item['reviews'] = self.text_processing(reviews)
        
        yield item

