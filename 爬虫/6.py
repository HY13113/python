import requests, re, time
import csv  # 导入csv模块用于保存数据
# 设置请求头，模拟浏览器访问
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
           'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://m.weibo.cn/u/3879109948',
           'Cookie': "_T_WM=91468834951; WEIBOCN_FROM=1110006030; SCF=AqTW0zSqyfcfZw-xTyN33PSH7SxpD_brTLHK4ix3WOJEkniwQ6rBaZ6zKF8G1s4lhzVmnxg8SKhaYH89oWy36Fc.; SUB=_2A25ELI6ZDeRhGeFJ7FcQ8C7OzD2IHXVnQ45RrDV6PUJbktANLXmjkW1NfzEPToO_b1XTL1PUDlX_Xibl_veoa8PY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFRdzSDHMqPJLWQlKGj-1.w5NHD95QNS0MfeK57eoMpWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0MNSK27ehzNeBtt; SSOLoginState=1764294345; ALF=1766886345; MLOGIN=1; XSRF-TOKEN=b29704; mweibo_short_token=759ed093c0; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076033879109948%26fid%3D1005053879109948%26uicode%3D10000011"
           }
# 微博API接口URL
url = "https://m.weibo.cn/api/container/getIndex"
# 请求参数：用户ID和容器ID
params = {"type": "uid", "value": "3879109948", "containerid": "1076033879109948", "page": 1}
# 初始化存储所有微博的列表
all_weibos = []
# 设置起始页码和最大页码
page, max_page = 1, 5
print("开始抓取微博...")
# 循环抓取多页微博数据
while page <= max_page:
    params["page"] = page  # 设置当前页码
    print(f"第{page}页", end=" ")
    # 发送GET请求获取微博数据
    r = requests.get(url, headers=headers, params=params)
    data = r.json()  # 解析返回的JSON数据
    # 从返回数据中提取微博卡片列表
    cards = data.get('data', {}).get('cards', [])
    # 遍历每个卡片，筛选出微博内容卡片（card_type为9）
    for card in cards:
        if card.get('card_type') == 9:
            mblog = card.get('mblog', {})  # 获取微博详细信息
            # 直接使用原始文本，不进行数据清洗
            text = mblog.get('text', '')
            # 将微博信息添加到列表
            all_weibos.append({
                "time": mblog.get('created_at', ''),  # 发布时间
                "text": text,  # 微博内容
                "repost": mblog.get('reposts_count', 0),  # 转发数
                "comment": mblog.get('comments_count', 0),  # 评论数
                "like": mblog.get('attitudes_count', 0)  # 点赞数
            })
    print(f"成功，累计{len(all_weibos)}条")
    page += 1  # 页码加1
    time.sleep(1)  # 延迟1秒，避免请求过快
# 保存到CSV文件
csv_filename = "weibo_data.csv"
# 以UTF-8编码打开CSV文件，准备写入
with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as csvfile:
    # 定义CSV文件的列名
    fieldnames = ['时间', '内容', '转发数', '评论数', '点赞数']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # 写入表头
    writer.writeheader()
    # 遍历所有微博数据，逐行写入CSV文件
    for weibo in all_weibos:
        writer.writerow({
            '时间': weibo['time'],
            '内容': weibo['text'],
            '转发数': weibo['repost'],
            '评论数': weibo['comment'],
            '点赞数': weibo['like']
        })
print(f"\n抓取完成，共{len(all_weibos)}条微博，已保存到{csv_filename}")
print("232226205122")