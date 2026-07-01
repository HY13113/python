import base64
import hashlib
import math
import random
import time
import pandas as pd
import requests
# 配置信息
url = 'https://piaofang.maoyan.com/dashboard-ajax/movie'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Referer': 'https://piaofang.maoyan.com/dashboard',
    'Cookie': '_lxsdk_cuid=19ac98cc9c7c8-011d53199a91c78-26011c51-1fa400-19ac98cc9c780; _lxsdk=19ac98cc9c7c8-011d53199a91c78-26011c51-1fa400-19ac98cc9c780; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=19ac98cc9c8-211-419-344%7C%7C2'
}
# 生成请求参数
ua_encoded = base64.b64encode(headers['User-Agent'].encode()).decode()
timestamp = str(math.ceil(time.time() * 1000))
index = str(round(random.random() * 1000))
sign_content = f"method=GET×tamp={timestamp}&User-Agent={ua_encoded}&index={index}&channelId=40009&sVersion=2&key=A013F70DB97834C0A5492378B1E8134"
sign = hashlib.md5(sign_content.encode()).hexdigest()
params = {
    'orderType': '0',
    'uuid': '17d79b87a00c8-015087c7514df4-5919145b-144000-17d79b87a00c8',
    'timestamp': timestamp,
    'User-Agent': ua_encoded,
    'index': index,
    'channelId': '40009',
    'sVersion': '2',
    'signKey': sign
}
# 发送请求并获取响应
resp = requests.get(url, headers=headers, params=params).json()
# 直接获取电影列表
movie_list = resp['movieList']['list']
# 数据字段映射 - 修正电影名称和上映时间的提取路径
data_map = [
    ('电影名称', 'movieInfo', 'movieName'),
    ('上映时间', 'movieInfo', 'releaseInfo'),
    ('综合票房', '', 'sumBoxDesc'),
    ('上座率', '', 'avgSeatView'),
    ('场均人次', '', 'avgShowView'),
    ('票房占比', '', 'boxRate'),
    ('排片场次', '', 'showCount'),
    ('排片占比', '', 'showCountRate')
]
# 提取数据
data = {}
for cn_name, parent_key, en_name in data_map:
    if parent_key:
        data[cn_name] = [movie[parent_key][en_name] for movie in movie_list]
    else:  # 直接提取的情况
        data[cn_name] = [movie[en_name] for movie in movie_list]
# 保存数据
pd.DataFrame(data).to_csv('猫眼电影数据.csv', index=False, encoding='utf-8')
print(f"成功保存 {len(movie_list)} 条电影数据")
print("232226205122")