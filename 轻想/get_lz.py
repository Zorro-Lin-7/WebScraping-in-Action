import pymongo
from qingxiang import lianzai_list
from qx_details import get_lz_info,client,lz_info
import pandas as pd
from multiprocessing import Pool
import time

df=pd.DataFrame(list(lianzai_list.find({},{'link':1})))
df['link']=df['link'].astype('str')



if __name__ == '__main__':
	for m in range(0,len(df['link']),125):
		pool=Pool()
		pool.map(get_lz_info,df['link'][m:m+125])
		pool.close()
		pool.join()
		print('暂停20秒...')
		time.sleep(20)
	print('Done')


#--------不采用多进程，使得原函数中的time.sleep有效--------    
# for url in df['link']:
# 	get_lz_info(url)
# 	
# print('Done')