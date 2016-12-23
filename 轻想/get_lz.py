import pymongo
from qingxiang import lianzai_list
from qx_details import get_lz_info,client,lz_info
import pandas as pd
from multiprocessing import Pool


df=pd.DataFrame(list(lianzai_list.find({},{'link':1})))
df['link']=df['link'].astype('str')


if __name__ == '__main__':
    pool=Pool()
    pool.map(get_lz_info,df['link'])
    pool.close()
    pool.join()
    print('Done')