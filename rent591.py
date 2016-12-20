from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
rent591 = client['rent591']
rent_info = rent591['rent-info']

def get_rent_info(url):
    browser = webdriver.Chrome()
    browser.get(url)
    soup=BeautifulSoup(browser.page_source,'lxml')
    count=0
    for i in range(1,185):
        titles=soup.select('h3 > span')
        urls = soup.select('a.shlist.clearfix')
        for title,url in zip(titles,urls):
            data = {'title':title.text,
                    'url':url.get('href')
                    }
            count=count+1
            print(data)
        print(count)
        rent_info.insert_one(data)
        browser.find_element_by_link_text(u"下一頁").click()
        time.sleep(2)  # 必须延时
        soup=BeautifulSoup(browser.page_source,'lxml')


get_rent_info('https://rent.591.com.hk')