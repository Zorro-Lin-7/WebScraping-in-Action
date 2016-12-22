import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import pymongo

client=pymongo.MongoClient('localhost',27017)
qingxiang = client['qingxiang']
lz_info = qingxiang['lz_info']
witness = qingxiang['witness']

# 进入连载链接，获取详情信息：博主名字、连载名称、连载描述、所属标签、热度、见证人数
# 从mongoDB中取出链接url
def get_lz_info(url):
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
    print(details)


# 获取（见证人）用户信息：轻想号及个人主页、昵称

def get_user_info(url):
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
        witness_info = requests.post(w,data=data)
        witness_info = json.loads(witnessme.text)
        witness_info=pd.DataFrame(wt['results']).to_dict()
        witness.insert_one(witness_info)
    else:
        print('无人见证')


