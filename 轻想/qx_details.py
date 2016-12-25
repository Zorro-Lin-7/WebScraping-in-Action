import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import pymongo
import json
import random

client=pymongo.MongoClient('localhost',27017)
qingxiang = client['qingxiang']
lz_info = qingxiang['lz_info']
witness = qingxiang['witness']

# 进入连载链接，获取详情信息：博主昵称、连载标题、连载描述、所属标签、热度、见证人数、连载号、用户id
# 从mongoDB中取出链接url

headers={'Connection':'keep-alive',
	'Host':'www.lianzai.me',
	'Referer':'http://www.lianzai.me/planList/1.html',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

proxy_list=[
    'http://125.88.74.122:83',
    'http://111.13.109.27:80',
    'http://111.13.7.42:81'
    ]


# 目标对象是活跃用户，活跃表现为发连载和参与见证，所以以行为标的——连载为单位进行挖掘，而不是用户（因为用户可能流失、不活跃）
def get_lz_info(url,i=150,t1=10,t2=0):  # 预设每爬取i=150 条暂停t1=10秒
	try:
		proxy_ip=random.choice(proxy_list)
		proxies={'http':proxy_ip}
		print('此时代理IP为： ',proxies)
		wb_data=requests.get(url,headers=headers,proxies=proxies,timeout=3)
	except:
		print('代理IP {}连接超时，切换继续'.format(proxy_ip))
		wb_data=requests.get(url,headers=headers)
	wb=wb_data.text
	soup=BeautifulSoup(wb,'lxml')
	error=0
	try:
		nickname=soup.select('h4')[0]     
		title=soup.select('div.base-info-content > h1')[0]
		description=soup.select('p.description')[0]
		tags=soup.select('#plantags > ul')[0]
		hot=soup.select('div.active-area-oper > span')[0]
		witness=soup.select('li.plan-witness > div > span')[0]
		ids = re.search(r'(\d+)/(\d+)', url)
		details = {
			'url':url,
			'uid':ids.group(1),
			'planId':ids.group(2),
			'nickname': nickname.text.strip(),
			'title':title.text.strip(),
			'description': description.text.strip(),
			'tags': list(tags.stripped_strings),
			'hot': hot.text,
			'witness': witness.text}
		lz_info.insert_one(details)
		print(details)
	except IndexError:
		error=error+1
		pass
	if lz_info.find().count() % i ==0:  #通过查看数据库记录，爬取一定数量后暂停较长时间再继续
		print('此时数据库记录为：',lz_info.find().count()) 
		print('暂停{}秒'.format(str(t1)))
		time.sleep(t1)  	       #推迟调用线程的运行，对于多进程好像无效
	else:
		time.sleep(t2)
	print("error: ",error)
	

# 从每个连载里挖取（见证人）用户信息：轻想号及昵称

def get_user_info(url,i=200,t1=12,t2=0):
	print(url)
	try:	
		
		proxy_ip=random.choice(proxy_list)
		proxies={'http':proxy_ip}
		print('此时代理IP为： ',proxies)
		wb_data = requests.get(url,proxies=proxies,timeout=3)
	except:
		print('代理IP {}连接超时，切换继续'.format(proxy_ip))
		wb_data = request.get(url)
	wb = wb_data.text
	soup = BeautifulSoup(wb, 'lxml')
	if int(soup.select('li.plan-witness > div > span')[0].text) != 0:
		#http: // www.lianzai.me / planDetail / 195563 / 96637.html?orderBy = 1
		ids = re.search(r'(\d+)/(\d+)', url)
		data={'uid':ids.group(1),
               'pageSize':50,
              'planId':ids.group(2)}
		w='http://www.lianzai.me/lianzai/WitnessCtrl/showWitnessMe'
		headers={
				'Cookie':'Hm_lvt_93e1b0e22c390a517a33b4e510d6fc16=1482361423,1482404873,1482450043,1482473049; Hm_lpvt_93e1b0e22c390a517a33b4e510d6fc16=1482476200; PLAY_ERRORS=',
				'Host':'www.lianzai.me',
				'Origin':'http://www.lianzai.me',
				'Referer':url,
				'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
				'X-Requested-With':'XMLHttpRequest'
				}
		witness_info = requests.post(w,data=data,headers=headers)
		witness_info = json.loads(witness_info.text)
        #print(pd.DataFrame(witness_info))
		witness.insert_one(witness_info)   # mongoDB只能存字典格式，而且其中的key必须是str。原先提炼信息后用df.to_dict，df索引是数值，
                                                            #key也就变为数值，无法存入
		if witness.find().count() % i ==0:
			time.sleep(t1)
			print('此时数据库记录为：',lz_info.find().count()) 
			print('暂停{}秒'.format(str(t1)))
		else:
			time.sleep(t2)
        #witness_info=pd.DataFrame(witness_info['results'])
        #print(witness_info)
	else:
		print('无人见证')
        
    
