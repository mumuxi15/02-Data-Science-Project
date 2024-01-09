Initially started the project in 2018, updated in 2021. 

#### Updates in 2021

------

In the 2018, I scraped 5000 anime and 5000 users information from MyAnimeList. Almost 4 year later, I found a data source on kaggle - [Anime Recommendation Database](https://www.kaggle.com/CooperUnion/anime-recommendations-database) including 73,516 users on 12,294 anime. That's why I decided to review the project and improve the algorithm and code efficiency.  Here are the updates

1. Rewrite README and add more details 
1. Recode scrapy part and complete the kaggle data set with more features
1. Did more research on recommender and came up with a few suggestions
1. Improve the code and run on the new data set. 
1. Test those suggestions





## Introduction







## Challenge



## Data Preparation - Scraping

###### Preparation: Install Python packages

Scrapy, Pymongo, nltk

###### [Mac IOS] Check if Mongodb is installed 

```shell
mongo --version                         # check if installed
brew tap mongodb/brew                   #if not: homebrew download package
brew install mongodb-community          #install
brew services start mongodb-community   #start
```

###### Scrape data from MyAnime list and output to Mongodb

Get listed anime id and use those to generate url links to get additional anime information such as storyline, producers, reviews etc via scrapy

```shell
cd anime_scrawler
scrapy crawl anime #save data to mongodb
scrapy crawl anime -o output.json   # output to json file
```

###### Mongo shell

```shell
show dbs
use items
db.anime_items.find().limit(3)
quit()
```

###### Deal with duplicates 

Option A. Mongo shell

```shell
""" check if duplicates exist """
db.anime_items.count()                #count doc num in collection
db.anime_items.distinct("id").length  # count distinct

"""if counts not match """
db.anime_items.aggregate([
 {
     "$group": {
         _id: {id: "$id"},
         dups: { $addToSet: "$_id" } ,
         count: { $sum : 1 }
     }
 },
 {
     "$match": {
         count: { "$gt": 1 }
     }
 }
]).forEach(function(doc) {
   doc.dups.shift();
   db.anime_items.remove({
       _id: {$in: doc.dups}
   });
})
```

 Option B. Pymongo

```python
'''anime_scrawler/pipeline.py'''
def process_item(self, item, spider):
#   'check if id exist before insertion to avoid duplicates'
    if self.db[self.collection_name].find({"id" : item["id"]}).count() > 1:
        pass
    else:
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
    return item
```





## Model Architecture



<img style="width:100%;display:block;" src="https://i.imgur.com/zBbWj8p.jpg">

## Model Performance



###### 

## Reference

To better understand recommender system, I highly recommend reading the Netflix prize winner's team Yehuda Koren, Yahoo Research Robert Bell and Chris Volinsky, AT&T Labs' work: *Matrix Factorization Technique for Recommender System* (https://datajobs.com/data-science-repo/Recommender-Systems-[Netflix].pdf)
