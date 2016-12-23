import pymongo
from qx_details import get_lz_info,get_user_info
from qingxiang import lianzai_list,client
from qx_details import witness
from multiprocessing import Pool
import pandas as pd

df=pd.DataFrame(list(lianzai_list.find({},{'link':1})))
df['link']=df['link'].astype('str')
#print(df['link'])

if __name__ == '__main__':
    pool=Pool()
    #pool.map(get_lz_info,df['link'])
    pool.map(get_user_info,df['link'])
    pool.close()
    pool.join()
    print('Done')