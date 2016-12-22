import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
qingxiang = client['qingxiang']
lianzai_list = qingxiang['lianzai_list']


# 获取某页的所有连载链接，返回title和link
def get_links(url):
    base_url='http://www.lianzai.me'
    wb_data=requests.get(url)
    wb=wb_data.text
    soup=BeautifulSoup(wb,'lxml')
    links=soup.select('a.cover-wrap')
    titles=soup.select('p.title')
    for title,link in zip(titles,links):
        data={
            'title':title.text.strip(),
            'link':base_url+str(link.get('href'))
        }
        lianzai_list.insert_one(data)
        print(data)
# 在版块'最新'下翻页，获取全部链接
def get_more_pages(start,end):
    urls = ['http://www.lianzai.me/planList/{}.html'.format(str(page)) for page in range(start,end)]
    for p in urls:
        print('第{}页'.format(str(p)))
        get_links(p)
        time.sleep(2)



