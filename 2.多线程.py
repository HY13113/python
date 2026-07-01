import time
import requests
import re
from multiprocessing.dummy import Pool
from pymongo import MongoClient
start = time.time()
client = MongoClient()
db = client.novel_db
# 获取章节链接
html = requests.get('http://www.newxue.com/mingzhujianshang/maitianlideshouwangzhe').content.decode('gbk')
urls = re.findall('<div class="xslttext">(.*?)</div>', html, re.S)[0]
urls = re.findall('<a href="(.*?)"', urls, re.S)[:10]
def crawl(url):
    url = 'http://www.newxue.com' + url if url.startswith('/') else url
    # 获取页面
    page = requests.get(url).content.decode('gbk')
    # 提取标题
    title = re.findall('id="bktitle">(.*?)</p>', page, re.S)
    title = title[0].strip() if title else '未知标题'
    # 提取内容
    content = re.findall('<div id="dashu_text">(.*?)</div>', page, re.S)
    if not content:
        content = re.findall('<div class="content"[^>]*>(.*?)</div>', page, re.S)
    content = content[0] if content else ''
    # 保存
    db.maitian_shouwang_multi.insert_one({'title': title, 'content': content, 'url': url})
    return "成功: " + title
# 多线程爬取
for result in Pool(4).map(crawl, urls):
    print(result)
total_time = time.time() - start
print("多线程爬虫总耗时: %.2f秒" % total_time)
print("学号：232226205122")