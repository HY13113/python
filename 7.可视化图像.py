import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
# 设置中文字体 - 解决matplotlib显示中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
def clean_box_data(box_str):
    """清洗票房数据 - 将带单位的票房字符串转换为数值（单位：万元）"""
    # 处理空值或无效值
    if pd.isna(box_str) or box_str in ['--', '', '未知']:
        return None

    # 处理以"亿"为单位的票房数据
    if '亿' in str(box_str):
        num = re.findall(r'(\d+\.?\d*)', str(box_str))  # 提取数字部分
        return float(num[0]) * 10000 if num else None  # 1亿 = 10000万元
    # 处理以"万"为单位的票房数据
    elif '万' in str(box_str):
        num = re.findall(r'(\d+\.?\d*)', str(box_str))
        return float(num[0]) if num else None
    return None
def clean_percent_data(percent_str):
    """清洗百分比数据 - 将百分比字符串转换为小数"""
    if pd.isna(percent_str) or percent_str in ['--', '', '未知']:
        return None
    try:
        # 去除百分号并转换为小数
        return float(str(percent_str).replace('%', '')) / 100
    except:
        return None
# 读取数据
try:
    # 从CSV文件读取电影数据
    df = pd.read_csv('猫眼电影数据.csv', encoding='utf-8')
    print('成功读取数据，数据量：', len(df))
except:
    print('读取数据失败')
    exit()
# 数据清洗和转换
# 将票房字符串转换为数值（万元）
df['总票房(万元)'] = df['综合票房'].apply(clean_box_data)
# 将百分比字符串转换为小数
df['上座率_数值'] = df['上座率'].apply(clean_percent_data)
df['票房占比_数值'] = df['票房占比'].apply(clean_percent_data)
df['排片占比_数值'] = df['排片占比'].apply(clean_percent_data)
# 将数值列转换为数值类型，无法转换的设为NaN
df['场均人次_数值'] = pd.to_numeric(df['场均人次'], errors='coerce')
df['排片场次_数值'] = pd.to_numeric(df['排片场次'], errors='coerce')
# 过滤有效数据 - 只保留有票房数据且票房大于0的记录
valid_df = df[df['总票房(万元)'].notna() & (df['总票房(万元)'] > 0)].copy()
# 按票房降序排列，取前20名
top20_df = valid_df.sort_values('总票房(万元)', ascending=False).head(20)
# 检查是否有有效数据
if top20_df.empty:
    print('无有效数据')
    exit()
# 统计信息计算
# 选择数值列进行描述性统计
stats_df = valid_df[['总票房(万元)', '上座率_数值', '场均人次_数值', '票房占比_数值', '排片占比_数值']].describe()
# 重命名统计指标为中文
stats_df.index = ['总数', '均值', '标准差', '最小值', '25%分位数', '中位数', '75%分位数', '最大值']
print('\n统计信息：')
print(stats_df.round(4))  # 保留4位小数
print('\nTOP20电影：')
# 显示前20名电影的关键信息
print(top20_df[['电影名称', '综合票房', '上座率', '场均人次']].round(2))
# 数据可视化
# 创建2行1列的子图，设置图形大小
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
# 第一个子图：票房柱状图
x = top20_df['电影名称']
y = top20_df['总票房(万元)'] / 10000  # 转换为亿元单位
# 绘制柱状图
bars = ax1.bar(range(len(x)), y, color='#2E86AB', alpha=0.8)
ax1.set_title('TOP20电影票房排行', fontsize=16, fontweight='bold')
ax1.set_ylabel('票房（亿元）')
# 设置x轴刻度和标签
ax1.set_xticks(range(len(x)))
ax1.set_xticklabels(x, rotation=45, ha='right')  # 旋转45度，右对齐
ax1.grid(axis='y', linestyle='--', alpha=0.7)  # 添加网格线
# 在柱状图上添加数值标签
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}',
             ha='center', va='bottom', fontsize=8)
# 第二个子图：散点图（场均人次 vs 上座率）
# 过滤掉有空值的数据
scatter_df = top20_df[top20_df['场均人次_数值'].notna() & top20_df['上座率_数值'].notna()]
if not scatter_df.empty:
    # 绘制散点图
    ax2.scatter(scatter_df['场均人次_数值'], scatter_df['上座率_数值'] * 100,  # 上座率转换为百分比
                s=100, c='#A23B72', alpha=0.7)  # 设置点的大小和颜色
    ax2.set_title('场均人次 vs 上座率', fontsize=16, fontweight='bold')
    ax2.set_xlabel('场均人次')
    ax2.set_ylabel('上座率（%）')
    ax2.grid(linestyle='--', alpha=0.7)
# 调整子图间距
plt.tight_layout()
# 保存图表为PNG文件
plt.savefig('电影分析图.png', dpi=300, bbox_inches='tight')
plt.show()
# 创建饼图显示票房占比
plt.figure(figsize=(10, 8))
# 取前10名电影制作饼图
top10_df = top20_df.head(10)
# 绘制饼图，显示百分比
plt.pie(top10_df['总票房(万元)'], labels=top10_df['电影名称'], autopct='%1.1f%%')
plt.title('TOP10电影票房占比')
plt.tight_layout()
# 保存饼图
plt.savefig('票房占比饼图.png', dpi=300, bbox_inches='tight')
plt.show()
print('图表保存完成')
print("232226205122")