import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
qingxiang = client['qingxiang']
lianzai_list = qingxiang['lianzai_list']

headers={
'Connection':'keep-alive',
'Cookie':'Hm_lvt_93e1b0e22c390a517a33b4e510d6fc16=1482361423,1482404873,1482450043,1482473049; Hm_lpvt_93e1b0e22c390a517a33b4e510d6fc16=1482474900; PLAY_ERRORS=',
'Host':'www.lianzai.me',
'Referer':'http://www.lianzai.me/planList/1.html',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
# 获取某页的所有连载链接，返回title和link
def get_links(url):
    base_url='http://www.lianzai.me'
    wb_data=requests.get(url,headers=headers)
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
        print('网页{}下的链接：'.format(str(p)))
        get_links(p)
        time.sleep(1.5)


# get_more_pages(1,200)
