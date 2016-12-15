import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
test = client['test']
ganji_item_urls = test['ganji_item_urls']
ganji_item_info = test['ganji_item_info']

# spider 1 :抓取指定类目下，指定某页"来自转转"的产品连接，并存到mongoDB

def get_items_link(channel_link,page):
    if page>1:
        url = '{}o{}/'.format(channel_link,str(page))
    else:
        url = channel_link
    wb_data = requests.get(url)
    time.sleep(1.5)
    wb = wb_data.text
    soup = BeautifulSoup(wb,'lxml')
    # 若页面没有产品
    if soup.find('td','t'):
        items = soup.select('tr.zzinfo > td.t > a')
        for item in items:
            item_link = item.get('href').split('?')[0]
            ganji_item_urls.insert_one({'item_link':item_link})
            print(item_link)
    else:
        pass


#spider 2 ：抓取每个产品详情页里的信息，并存到mongoDB
# 爬取1个item
# 爬取所有items

def get_item_info(item_url):
    wb_data = requests.get(item_url)
    wb = wb_data.text
    time.sleep(1.5)
    soup = BeautifulSoup(wb,'lxml')

    title = soup.select('h1.info_titile')[0].text
    price = soup.select('div.price_li > span > i')[0].get_text()
    area = soup.select('div.palce_li > span > i')[0].text
    quality = [i.text for i in soup.select('span.qual_label')]

    data = {
        'title':title,
        'price':price,
        'area':area,
        'quality':quality,
        'item_url':item_url
    }
    ganji_item_info.insert_one(data)
    print(data)


