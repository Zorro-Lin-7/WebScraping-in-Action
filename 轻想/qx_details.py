import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import pymongo
import json

client=pymongo.MongoClient('localhost',27017)
qingxiang = client['qingxiang']
lz_info = qingxiang['lz_info']
witness = qingxiang['witness']

# 进入连载链接，获取详情信息：博主名字、连载名称、连载描述、所属标签、热度、见证人数
# 从mongoDB中取出链接url


def get_lz_info(url,i=200,t1=10,t2=0):  # 预想每爬取i=200 条暂停t1=10秒

    wb_data=requests.get(url)
    wb=wb_data.text
    soup=BeautifulSoup(wb,'lxml')

    nickname=soup.select('h4')[0]
    title=soup.select('div.base-info-content > h1')[0]
    description=soup.select('p.description')[0]
    tags=soup.select('#plantags > ul')[0]
    hot=soup.select('div.active-area-oper > span')[0]
    witness=soup.select('li.plan-witness > div > span')[0]
    
    details = {
        'nickname': nickname.text.strip(),
        'title':title.text.strip(),
        'description': description.text.strip(),
        'tags': list(tags.stripped_strings),
        'hot': hot.text,
        'witness': witness.text}
    lz_info.insert_one(details)
    
    if lz_info.find().count() % i ==0:  #通过查看数据库记录，爬取一定数量后暂停较长时间再继续
    	time.sleep(t1)
    else:
    	time.sleep(t2)
    	
    
    print(details)
	

# 获取（见证人）用户信息：轻想号及个人主页、昵称

def get_user_info(url,i=200,t1=12,t2=0):
	print(url)
	wb_data = requests.get(url)
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
		else:
			time.sleep(t2)
        #witness_info=pd.DataFrame(witness_info['results'])
        #print(witness_info)
	else:
		print('无人见证')
        
    
