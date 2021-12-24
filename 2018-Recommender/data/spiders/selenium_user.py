#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium import webdriver
#import time
#import pickle
#driver = webdriver.Chrome('/Users/mumuxi/chromedriver')
#userlst = []
#
#for i in range(260):
#    try:
#        driver.get("https://myanimelist.net/users.php")
#        time.sleep(1)
#        username = driver.find_elements_by_xpath('//div[@style="margin-bottom: 7px;"]/a')
#        for user in username:
#            userlst.append(user.get_attribute("href"))
##        input_element.send_keys(mv+" movie")
#    except:
#        print ('TimeoutError',i)
#        driver = webdriver.Chrome('/Users/mumuxi/chromedriver')
#        pass
#userlst = list(set(userlst))
#pickle.dump(userlst[0:5000], open( "userlst.p", "wb"))
    
    




