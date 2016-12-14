from channel_extract import channel_list
from spiders import get_items_link
from multiprocessing import Pool

def get_all_item_links(channel):
    for i in range(1,101):
        get_items_link(channel,i)



if __name__=='__main__':
    pool=Pool()
    pool.map(get_all_item_links,channel_list.split())
