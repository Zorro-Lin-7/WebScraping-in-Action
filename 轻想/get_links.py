from qingxiang import get_more_pages
import time

for i in range(1,1278,200):
	get_more_pages(i,i+200)   # 每200页暂停12秒
	time.sleep(12)
	
time.sleep(20)	
get_more_pages(1201,1279)
print('Done')

# 最终只爬取到1004页