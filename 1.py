import re
import pandas as pd
# 读取所有页面内容
folder_path = "c:/Users/smile/PycharmProjects/PythonProject/爬虫/tieba_pages"
all_source = "\n".join(open(f"{folder_path}/{i}.txt", encoding='utf-8').read() for i in range(1, 6))
# 匹配帖子块
every_block = re.findall(
    r'<div class="l_post.*?data-field=.*?<div class="core_reply.*?</div></div></div>',
    all_source, re.S
)
print(f"共匹配到 {len(every_block)} 个帖子")
# 提取数据
data = []
for block in every_block:
    # 使用re.findall直接提取数据
    users = re.findall(r'<a data-field=.*?class="p_author_name.*?>(.*?)</a>', block, re.S)
    times = re.findall(r'date&quot;:&quot;(.*?)&quot;,&quot;', block, re.S)
    contents = re.findall(r'<div id="post_content_\d+".*?>(.*?)</div>', block, re.S)
    clients = re.findall(r'open_type&quot;:&quot;(.*?)&quot;', block, re.S)
    # 取第一个匹配结果（如果存在）
    user = users[0] if users else "未知用户"
    time = times[0] if times else "未知时间"
    content = contents[0] if contents else "无内容"
    client = clients[0] if clients else "网页版"
    data.append({
        "用户名": user,
        "发帖时间": time,
        "帖子内容": content,
        "客户端": client
    })

# 保存结果
pd.DataFrame(data).to_csv("tieba_5pages_all_data.csv", index=False, encoding="utf-8-sig")
print("5页内容提取完成，已保存到 tieba_5pages_all_data.csv")
print("学号：232226205122")