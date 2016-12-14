import time
from spiders import ganji_item_urls
while True:
    print(ganji_item_urls.find().count())
    time.sleep(5)