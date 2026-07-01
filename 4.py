import requests
import csv
import time
# 配置参数
TARGET_COUNT = 150  # 目标爬取评论数量
PAGE_SIZE = 20  # 每页请求的评论数量
OUTPUT_FILE = "bilibili_comments.csv"  # 输出文件名
# 请求头 - 模拟浏览器访问，避免被识别为爬虫
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",  # 浏览器标识
    "Referer": f"  ",  # 请求来源页面
    "Cookie": "buvid3=C62D1419-B285-B798-D382-B7DDECF4409932251infoc; b_nut=1764206032; b_lsid=D4C9A10D2_19AC2DFB6BF; _uuid=C5849F510-EBFE-2921-410A3-719FD101D7C31032580infoc; CURRENT_FNVAL=4048; CURRENT_QUALITY=0; buvid4=72A7C798-7DBE-DD24-5151-BE8601BFB2B332872-025112709-nPTa9e2+x7syP48/MvYKkg%3D%3D; buvid_fp=887a1341c55eaba164e313380000ce52; rpdid=|(JY~|JlkRll0J'u~YRk|Y|JJ; csrf_state=7d2351c2e5b3a7f4e0438d89f509ce72; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInT5cCI6IkpXVCJ9.eyJleHAiOjE3NjQ0NjUyMzksImlhdCI6MTc2NDIwNTk3OSwicGx0IjotMX0.gt5shY_g-egSLUiIhpeAFVJk4HaMWyYX0omNS6WwwQo; bili_ticket_expires=1764465179; SESSDATA=9fefdb93%2C1779758040%2Cacec8%2Ab1CjC4AsTLFKQTHPvlBCQSoKIqUHAuZFMHnXA9kcY4Jazy__cPj510W3Y10CFCClGLkTsSVnRQXzlwam9KdDRJYk5idWtMdWtrQ1BvRlZRYXYtcVJWdXFSbVRSVVRYQW1kWEZ6SmpHTVFYajRwdXZZZV9GWHNpc0N4bVJsTUZLU1JReVdKRlVoempnIIEC; bili_jct=c18d1eacdeabfd601374c28d430ff287; DedeUserID=311803606; DedeUserID__ckMd5=33800358d0532c10; sid=4wh4sz7o; theme-tip-show=SHOWED"
    # 用户认证信息
}
# ========== 第一步：获取视频ID ==========
# 通过BV号获取视频详细信息，从中提取aid（视频ID）
url = f"https://api.bilibili.com/x/web-interface/view?bvid=BV1eiy3BYEvo"
response = requests.get(url, headers=HEADERS)  # 发送GET请求获取视频信息
oid = response.json()["data"]["aid"]  # 从返回的JSON数据中提取视频ID
# ========== 第二步：爬取评论 ==========
comments = []  # 用于存储所有评论的列表
page = 1  # 从第一页开始爬取
# 循环爬取直到达到目标数量或没有更多评论
while len(comments) < TARGET_COUNT:
    # 构造评论API的URL，包含视频ID、页面和每页数量参数
    comment_url = f"https://api.bilibili.com/x/v2/reply/main?oid={oid}&type=1&page_num={page}&page_size={PAGE_SIZE}"
    try:
        time.sleep(1)  # 每次请求后暂停1秒，避免请求过快被限制
        resp = requests.get(comment_url, headers=HEADERS)  # 发送请求获取评论
        data = resp.json()  # 解析返回的JSON数据
        # 从返回数据中提取评论列表，如果没有评论则终止循环
        replies = data["data"].get("replies", [])
        if not replies:
            break
        # 遍历当前页的所有评论
        for reply in replies:
            # 提取评论的关键信息：用户名、用户ID、评论内容、点赞数、回复数
            comment = [
                reply["member"]["uname"],  # 用户名
                reply["member"]["mid"],  # 用户ID
                reply["content"]["message"],  # 评论内容
                reply["like"],  # 点赞数
                reply["rcount"]  # 回复数
            ]
            comments.append(comment)  # 将评论添加到列表中
            # 如果已达到目标数量，则终止内部循环
            if len(comments) >= TARGET_COUNT:
                break
        page += 1  # 准备爬取下一页
    except:
        break  # 如果发生错误，终止循环
# 截取目标数量的评论，确保不会超过设定值
comments = comments[:TARGET_COUNT]
# ========== 第三步：保存到CSV文件 ==========
with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)  # 创建CSV写入器
    writer.writerow(['用户名', '用户ID', '评论内容', '点赞数', '回复数'])  # 写入表头
    writer.writerows(comments)  # 写入所有评论数据
# 输出结果
print(f"完成！保存{len(comments)}条评论")