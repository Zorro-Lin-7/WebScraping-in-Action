import requests
from bs4 import BeautifulSoup
import time
import pymongo
import random

client = pymongo.MongoClient('localhost',27017)
qingxiang = client['qingxiang']
lianzai_list = qingxiang['lianzai_list']

#http://cn-proxy.com/
proxy_list = [
    'http://101.200.169.110:80',
    'http://120.27.113.72:8888',
    'http://119.29.232.113:3128'
    ]


headers={
'Connection':'keep-alive',
'Host':'www.lianzai.me',
'Referer':'http://www.lianzai.me/planList/1.html',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
# 获取某页的所有连载链接，返回title和link
def get_links(url):
    base_url='http://www.lianzai.me'
    try:
    	proxy_ip=random.choice(proxy_list) # 随机获取代理ip
    	proxies={'http':proxy_ip}
    	print('代理ip为：',proxies)
    	wb_data=requests.get(url,headers=headers,proxies=proxies,timeout=3)
    except:
    	print('代理IP {}连接超时，切换'.format(proxy_ip))
    	wb_data=request.get(url)
    wb=wb_data.text
    soup=BeautifulSoup(wb,'lxml')
    links=soup.select('a.cover-wrap')
    titles=soup.select('p.title')
    for title,link in zip(titles,links):
    	data={
    	'title':title.text.strip(),
    	'link':base_url+str(link.get('href'))}
    	lianzai_list.insert_one(data)
    	print(data)
# 在版块'最新'下翻页，获取全部链接
def get_more_pages(start,end):
	urls = ['http://www.lianzai.me/planList/{}.html'.format(str(page)) for page in range(start,end)]
	for p in urls:
		if soup.find('section'):	#判断是否是最后一页
			print('网页{}下的链接：'.format(str(p)))
			get_links(p)
			time.sleep(1)
		else:
			break


# get_more_pages(1,200)
