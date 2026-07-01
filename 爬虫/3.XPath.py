import requests
import pandas as pd
import time
from lxml import etree  # 导入lxml的etree模块用于XPath解析
# 基础URL和请求头
base_url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": 'bid=kksxN5yN7BY; dbcl2="292432665:w/+D1eZjOsA"; _pk_id.100001.4cf6=c7ec5c21c4c0df1c.1764147525.; __utmz=30149280.1764147525.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1764147525.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; __yadk_uid=drI6jJqdkLfFJraxLadXycymfQXablKN; ll="118254"; _vwo_uuid_v2=D92F134669674B30D213A80ADF537BA51|d1fc4fd180ff5d198ce849d2392fd601; ck=pu_5; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1764493605%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1; __utma=30149280.604573563.1764147525.1764164545.1764493605.4; __utmb=30149280.0.10.1764493605; __utmc=30149280; __utma=223695111.723727574.1764147525.1764164545.1764493605.4; __utmb=223695111.0.10.1764493605; __utmc=223695111; frodotk_db="f87e15c93d47e619e97a415bb7d7b24b"'
}
# 初始化列表存储所有页面的电影数据（更换标签名）
movie_names = []
movie_infos = []
movie_scores = []
review_counts = []
plot_summaries = []
award_records = []
# 爬取10页内容，豆瓣TOP250每页25条，start参数从0开始，每次+25
for page in range(10):
    start = page * 25  # 分页参数：0,25,50...225（第10页）
    url = f"{base_url}?start={start}&filter="  # 构造分页URL
    print(f"\n开始爬取第{page + 1}页，URL：{url}")
    # 发送当前页的请求并解析（替换为lxml的etree解析）
    response = requests.get(url, headers=headers, timeout=10)
    # 将响应内容转换为lxml的Element对象，用于XPath查询
    html = etree.HTML(response.content.decode())
    # 获取当前页所有电影项的节点列表（对应原CSS的ol.grid_view li div.item）
    movie_items = html.xpath('//ol[@class="grid_view"]/li/div[@class="item"]')
    # 循环提取当前页的每部电影信息（使用新的变量名）
    for item in movie_items:
        # 电影标题（对应原span.title）
        title = item.xpath('.//span[@class="title"][1]/text()')[0].strip()
        movie_names.append(title)
        # 电影基本信息（对应原div.bd p:nth-of-type(1)）
        # 提取p标签下的所有文本并拼接
        info_texts = item.xpath('.//div[@class="bd"]/p[1]/text()')
        info = ' '.join([text.strip() for text in info_texts if text.strip()])
        movie_infos.append(info)
        # 电影评分（对应原span.rating_num）
        rating = item.xpath('.//span[@class="rating_num"]/text()')[0].strip()
        movie_scores.append(rating)
        # 评价人数（对应原div.bd div span最后一个）
        people = item.xpath('.//div[@class="bd"]/div/span[last()]/text()')[0].strip()
        review_counts.append(people)
        # 详情页链接
        detail_url = item.xpath('.//div[@class="hd"]/a/@href')[0]
        # 访问详情页
        time.sleep(1)
        detail_response = requests.get(detail_url, headers=headers, timeout=10)
        detail_html = etree.HTML(detail_response.content.decode())
        # 剧情简介（对应原span[property="v:summary"]）
        summary_texts = detail_html.xpath('//span[@property="v:summary"]/text()')
        summary = ' '.join([text.strip() for text in summary_texts if text.strip()]) if summary_texts else ""
        plot_summaries.append(summary)
        # 获奖情况（对应原ul.award下的所有文本）
        awards_texts = detail_html.xpath('//ul[@class="award"]//text()')
        awards_text = ' '.join([text.strip() for text in awards_texts if text.strip()]).strip()
        award_records.append(awards_text if awards_text else "暂无获奖信息")
        print(f"得到《{title}》的详细信息")
# 构建DataFrame并保存CSV
result = {
    '电影名称': movie_names,
    '基本信息': movie_infos,
    '豆瓣评分': movie_scores,
    '评价人数': review_counts,
    '剧情简介': plot_summaries,
    '获奖记录': award_records
}
df = pd.DataFrame(result)
df.to_csv("douban_top250_Xpath_232226205122.csv", encoding="utf_8_sig", index=False)
print(f"\n数据爬取完成！共获取{len(movie_names)}部电影信息")
print("文件已保存为: douban_top250_Xpath_232226205122.csv")
print("学号232226205122")