import requests
import csv
from datetime import datetime
import re
import warnings
warnings.filterwarnings("ignore")  # 忽略SSL警告
QUESTION_ID = "292977484"
LIMIT = 20  # 每页条数
OFFSET = 0  # 分页偏移量
# 知乎标准回答列表API
url = f"https://www.zhihu.com/api/v4/questions/292977484/answers"
params = {
    "include": "data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled",
    "offset": OFFSET,
    "limit": LIMIT,
    "order": "default",
    "platform": "web"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Cookie": '_zap=9914c6f9-5e19-4f23-bb90-416574d935c6; _xsrf=63d26e57-3f31-4dc0-87d9-e6c73e31105c; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1764657930; HMACCOUNT=BFDF2F1CA6451184; d_c0=GoeU5nKHdxuPTt1x1IcLZAFI3Dela54Fqcg=|1764657929; SESSIONID=Ry1ccwndvKWGJpaHELl8azWnrUEbXkWaTCFqKwsB6Tw; __snaker__id=KKatvlLiQYaod5Bl; JOID=V1ocAExj9C_HNIOBcmWxdzRJAvNlNoYUoFXz5BwXuHOKevHnMWV-D6gxj4B8bCxhZ6lYxylK9GbwT-nW_420btA=; osd=VVEWA0ph_yXEMoGKeGa3dT9DAfVnPYwXplf47h8RuniAefflOm99Cao6hYN6bidrZK9azCNJ8mT7RerQ_Ya-bdY=; DATE=1764657931182; cmci9xde=U2FsdGVkX1+zWYQVbC9TIaKEZFLOvni5CdqV/ilG0Nl02SGKDQy3K3Ncqd3a4tCE4973JqgE+weFECPsweXxeg==; pmck9xge=U2FsdGVkX180NT5DTgfVd18BKiEBN5hRvH8yU03Yjpw=; assva6=U2FsdGVkX1/OepXJOI0EBK4LNDQzvMnevzNSJ12qT68=; assva5=U2FsdGVkX19ulkjswbEY+3pnZ9YwgM5hzZpR0nGPmSR6Ap5xnk20ganQ2k81dNp43+CuKn0M/t1qMgXqy4breA==; gdxidpyhxdE=ExlPnchg7pDUNYwSbSmHaz77WMa7pHWYZdiKI%2Br8IZMMeqLxxEkqallxN%2BYO3wKSegwTTTbmT30QMZwUEtSIUI4J5MzhBJ8zVBe%5C4RdWqEHtW6ZblhsE8%2BsEQYtB7lJC4M1hIBCsBOvjDa5oHAs%2BiKrDGXDOE6BCbUuKySTAhnQO0VXy%3A1764658831347; crystal=U2FsdGVkX18tZXOCOfnbMPdg98NpuNSGSZojKtBB3AoSEpqK4mhUpbz1XfNVX9MdseoIZ92ayK45E3HXJA/dDaOhE56hBDnXyL2i8bGoEobYYBgnfRrEtjt9KnZK6QGQhm0Pk92AsYFeymfULXoYVN042AljyZl74wQPjC3oucJYPq2hlEixTOGHRw4VEWX8WnlO0liS3UN3PnJmKG7Uo/XSl8pu9MR6BbiMj1PMQGkNACWEeqxlqlJqFXWD6df/; vmce9xdq=U2FsdGVkX1+2dXOGouDfjKM9/7sUER2QZdgY8z5cuNitVb/x67Sh4CPC0fs6bmL/tuV1fhfJPQS7rtJB2q+8gLkqca8JsnMPzyL9zoz5r/P+46N7yIkyrnkXxvbbCsT2mpB7i2aj8xUrtW5cQ35Mq4fgPwLv59eF6WDlCh1y8RA=; captcha_session_v2=2|1:0|10:1764657932|18:captcha_session_v2|88:UjgyNU1zSXd6eGNOZW5sS1poSWlCckFCY2Y3VDcxbkRyYzdlK28yR3UzWi9PU240d3UydU5tR1czZzMzc1FYOQ==|f487ba9b994a4c4b0c21865d0b13726ff8628623776c0c437843416ca1f4b212; captcha_ticket_v2=2|1:0|10:1764658129|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfUTNvd25qT2hndypaNCpFWWxQdXNYMlNXLlNSd0phZVd3MEJxcFFNMFNGaHZkZnlwTzl4OHZ0R1JQWWt4OE1BZ2s4LnlqblN2dVROU3dUZk85a19JbXZWZjNPREVYQVF4T3RLTWRheUtGKjR2QzBBV2ozdk81M3EybDRvRG1MMDRGVm9zUXNGQ3NnOHJlWVhwQ1MuZUJvdTJja0VYdmwzVllTM3ZFWFd3cUhoVHRuVTM5Z1hOLkxyZktaYU80Mm9ENUxubkF4emJYKmwzdmdrRXFzUTZnWTB5cjNGdVoySVBtNFNnVmlIZUI4dXNoKip1RXphNXpGNHRXVmNLellqS3h0eDlFNlNkWkJsNUxJRFlxaWpfZWlyRHNMUEhIeWZUV09kZ1J4Q09XNWRLb0JvVEljdi4wQjZCQ245ZUJTbU9ickxHMmJOdWdLNDhPcWlsKk5obWpST2hPdGxMYy5hVG51VFhMS3BicU1jMVlsWG9UMHdvTW5PWW5PbWZXQjNaNnJMSXdlWFM4b09BcUhZVjJEYzFfS05ZKldVZ1VwVFNrem1rc19kRGg4dXpHUFd0X2cua2RpZHpJRzNrbmpiSFVfcEJzOXRvejNWejlCNkxZS2JxYXhrNVJtRW93KlFjNGdIeW9yc2hyaG9UeXBPVjIxM3VhZHEyZ2VxSDRBVllULm5sLlg3N192X2lfMSJ9|392f06fecb9335b62a8dd0cf589dd87eda76d8459531864bc1505580a33a8daa; z_c0=2|1:0|10:1764658129|4:z_c0|92:Mi4xZ1BpSFN3QUFBQUFhaDVUbWNvZDNHeVlBQUFCZ0FsVk4wZGtiYWdDMjROTF9SUFc4Vno1NHB3Y2loZ3B5WHF6NWh3|6cf05cc75e36e4bdb528119936901954062700f88638a721d787883f11b12bc9; q_c1=4cb37b63d2604a509ecb5ad2b0d32318|1764658130000|1764658130000; __zse_ck=004_ckPQm8c=lMbQMcgJyRog1nKIlm8dMD9g5KuTkkAf//1APHLRo0/X4clpcutJwAzyi1Ki9DfWSwPoqgCn3kWpRJ928CY8K=xu5ROQLCHdIU0/ozZ4GawWmfdoFQnYhOlA-Tugaw3fbBSS0MoelZbzjAm9dObPj/gbLRL2D+Imp5WkeHizrEn5J4Yahg3wOaCIbOBsxgKyMCoQlHHZNapp+jqNBaoUUe1UC6dlIIqv3Wf5yRDtQynJ24rsGl5zAezCO7u2lmh30KDVEIBu0Jf2PQ5bKcfMY/ixYv19HX3B9lsw=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1764658545; BEC=eee8906a1fecdebcee3fda89d6b84517',
    "Referer": 'https://www.zhihu.com/question/292977484',
}
# ====================== 发送API请求 ======================
response = requests.get(url, params=params, headers=headers)
if response.status_code != 200:
    print(f"请求失败！状态码：{response.status_code}，可能是Cookie失效或反爬拦截。")
    print("提示：检查Cookie是否有效，或添加更多请求头（如Origin）。")
    exit()
# 解析返回的JSON数据
data = response.json()
answers = data.get("data", [])
# ====================== 保存数据到CSV ======================
with open("wuhan_qa.csv", "w", newline="", encoding="utf-8-sig") as f:
    # 定义CSV表头并初始化写入器
    fieldnames = ["用户名", "回复内容", "回复时间"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    # 遍历每条回答，清理内容+转换时间后写入
    for ans in answers:
        # 直接清理回复内容（原clean_content函数逻辑）
        cleanr = re.compile('<.*?>')
        content = re.sub(cleanr, '', ans["content"]).strip().replace("\n", " ")
        # 直接转换时间戳（原format_timestamp函数逻辑）
        time_str = datetime.fromtimestamp(ans["created_time"]).strftime("%Y-%m-%d %H:%M:%S")
        # 写入CSV行
        writer.writerow({
            "用户名": ans["author"]["name"],
            "回复内容": content,
            "回复时间": time_str
        })
# 打印爬取结果提示
print(f"成功爬取 {len(answers)} 条数据，保存至 wuhan_qa.csv！")
print("232226205122")