from selenium import webdriver
from bs4 import BeautifulSoup

url = 'http://www.douyu.com/directory/all'
browser = webdriver.PhantomJS()   # 用PhantomJS 作浏览器
browser.get(url)                  # request动作
soup = BeautifulSoup(browser.page_source,'lxml')
count=0    #用于计数
while True:     # 一般已知总页数65，采用For循环更保险，这里为了熟悉selenium
    titles = soup.select('h3.ellipsis')
    tags = soup.select('span.tag.ellipsis')
    nums = soup.select('span.dy-num.fr')

    for title, tag, num in zip(titles,tags,nums):
        data = {
            'title':title.get_text().strip(),
            'tag':tag.get_text(),
            'num':num.get_text()
        }
        print(data)
        count = count + 1
    # 通过class进行定位，取到"下一页"这个控件，然后执行element的click()方法模拟鼠标点击
    elem = browser.find_element_by_class_name('shark-pager-next') # webdriver 的标签定位方法
    elem.click()

    if int(soup.select('a.shark-pager-item.current')[0].text)== 65:
        break
    soup = BeautifulSoup(browser.page_source, 'lxml')

print(count)