Initially started the project in 2018, updated in 2021. 

#### Updates in 2021

------

1. Find a data source on kaggle - [Anime Recommendation Database](https://www.kaggle.com/CooperUnion/anime-recommendations-database) inc 73,516 users on 12,294 anime
1. Rewrite README and add more details 
1. Recode scrapy part
1. Did more research on recommender and came up with a few suggestions
1. Test those suggestions



#### System Requirement

------

Database: MongoDB

Check if you have mongodb installed

On Mac: 

```
mongo --version                         # check if installed
brew tap mongodb/brew                   #homebrew download package
brew install mongodb-community@5.0      #install
```



Put in jupyter notebook later

Python packages: Scrapy, Pymongo, nltk

Download nltk libraries

```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```



#### Set up

------

Get additional anime information such as storyline, producers, reviews etc via scrapy

```shell
cd anime_scrawler
scrapy crawl anime #print to console
scrapy crawl anime -o output.json   # output to json file

```





#### Workflow

------

Detailed explanation can be found in my [blog](https://mumuxi15.github.io/) 

<img style="width:100%;display:block;" src="https://i.imgur.com/zBbWj8p.jpg">







