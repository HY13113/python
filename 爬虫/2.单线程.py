import requests
import re
import time
from pymongo import MongoClient
# 记录程序开始时间
start = time.time()
# 连接MongoDB数据库
client = MongoClient()
# 选择数据库
db = client.novel_db
# 获取小说目录页面，提取所有章节链接
html = requests.get('http://www.newxue.com/mingzhujianshang/maitianlideshouwangzhe').content.decode('gbk')
# 提取包含章节链接的div区域
urls = re.findall('<div class="xslttext">(.*?)</div>', html, re.S)[0]
# 从div区域中提取所有链接，并只取前10个
urls = re.findall('<a href="(.*?)"', urls, re.S)[:10]
# 遍历每个章节链接，爬取内容
for url in urls:
    # 补全URL（如果是相对路径则添加域名）
    url = 'http://www.newxue.com' + url if url.startswith('/') else url
    # 获取章节页面内容
    page = requests.get(url, timeout=10).content.decode('gbk')
    # 提取章节标题
    title = re.findall('id="bktitle">(.*?)</p>', page, re.S)
    title = title[0].strip() if title else '未知标题'
    # 提取章节内容，尝试两种可能的HTML结构
    content = re.findall('<div id="dashu_text">(.*?)</div>', page, re.S)
    if not content:
        content = re.findall('<div class="content"[^>]*>(.*?)</div>', page, re.S)
    content = content[0] if content else ''
    # 将数据插入MongoDB数据库
    db.maitian_shouwang.insert_one({'title': title, 'content': content, 'url': url})
    # 打印爬取进度
    print(f"已爬取: {title}")
# 计算总耗时
total_time = time.time() - start
# 输出结果
print("开始执行爬虫...")
print("完成，耗时: %.2f秒" % total_time)
print("学号：232226205122")