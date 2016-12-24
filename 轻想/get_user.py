import pymongo
from qx_details import get_lz_info,get_user_info
from qingxiang import lianzai_list,client
from qx_details import witness
from multiprocessing import Pool
import pandas as pd
import time

df=pd.DataFrame(list(lianzai_list.find({},{'link':1})))
df['link']=df['link'].astype('str')
#print(df['link'])

if __name__ == '__main__':
	for m in range(0,len(df['link']),105):
		pool=Pool()
		pool.map(get_user_info,df['link'][m:m+105])
		pool.close()
		pool.join()
		print('暂停20秒...')
		time.sleep(20)
		
	print('Done')