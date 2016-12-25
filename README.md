# WebScraping-in-Action
* [爬取赶集网二手市场所有类目下的产品信息](https://github.com/Zorro-Lin-7/WebScraping-in-Action/tree/master/ganjiwang)：近10万条链接,采取多进程爬取；用MongoDB存储
* [正则表达式精要](https://github.com/Zorro-Lin-7/WebScraping-in-Action/blob/master/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F.ipynb)  源自[Google For Edu](https://developers.google.com/edu/python/regular-expressions)
* [抓取淘宝网商品信息](https://github.com/Zorro-Lin-7/WebScraping-in-Action/blob/master/%E6%8A%93%E5%8F%96%E6%B7%98%E5%AE%9D%E5%95%86%E5%93%81%E4%BF%A1%E6%81%AF.ipynb)：淘宝网使用AJAX 方式填入页面内容。对此，从XHR 以及JS 切入，再使用正则表达式来抓取信息；并用pandas作数据规整
* [Pandas爬取中国银行外汇牌价信息](https://github.com/Zorro-Lin-7/WebScraping-in-Action/blob/master/pandas%E7%88%AC%E5%8F%96%E5%A4%96%E6%B1%87%E7%89%8C%E4%BB%B7.ipynb)：只用Pandas，只用Pandas，只用Pandas！
* [用PhantomJS+Selenium 处理斗鱼异步加载](https://github.com/Zorro-Lin-7/WebScraping-in-Action/blob/master/%E6%96%97%E9%B1%BCAJAX.py)：对于AJAX异步请求数据的网页，一个方式是通过url拼接，分页采集；另一个方法是使用Selenium。但发现Phantomjs 有点慢~~
* [爬取591租房信息（AJAX）](https://github.com/Zorro-Lin-7/WebScraping-in-Action/blob/master/rent591.py)：Selenium、MongoDB
* [“轻想”](https://github.com/Zorro-Lin-7/WebScraping-in-Action/tree/master/%E8%BD%BB%E6%83%B3)是一款类博客产品，从去年初创时作为种子用户，到现在成为深度用户，体会颇多。在此爬取全部用户数据并进行[数据分析](https://github.com/Zorro-Lin-7/WebScraping-in-Action/blob/master/%E8%BD%BB%E6%83%B3/%E8%BD%BB%E6%83%B3%E6%B4%BB%E8%B7%83%E7%94%A8%E6%88%B7%E9%87%8F%E5%88%86%E6%9E%90.ipynb)。过程中也遇到了几个问题：
 * 一开始用time.sleep进行间断访问，避免访问过于频繁引发反爬。结果用多进程操作时，才发现time.sleep对线程有效，对进程不阻塞。那么如何既用多进程又设置时间间隔？将整个过程分段，多进程爬取一段，暂停，再多进程爬取下一段。
 * ip代理问题。网上有些免费ip可能无效，无法进行request，遇到的情况是长时间在连接，也不弹出异常。这时用到了requests的timeout参数，若超时，就切换其他ip。
 * sleeptime
