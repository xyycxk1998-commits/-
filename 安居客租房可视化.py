import pandas as pd
import numpy as np
from pyecharts.charts import Bar, Line, Pie
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
import os

# 使用 CDN 加载 echarts
CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/"

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'yujinxq.csv')

# 读取数据
df = pd.read_csv(csv_path, encoding='gbk')

print("数据基本信息：")
print(df.info())
print("\n数据预览：")
print(df.head())
print(f"\n总数据量：{df.shape[0]} 条")

# 数据清洗
# 提取价格数值
df['价格'] = df['价格'].astype(str).str.extract('(\d+)').astype(float)
# 提取面积数值
df['面积'] = df['面积'].astype(str).str.extract('(\d+)').astype(float)
# 提取室的数量
df['室'] = df['户型'].astype(str).str.extract('(\d+)室').astype(float)
# 提取厅的数量
df['厅'] = df['户型'].astype(str).str.extract('(\d+)厅').astype(float)

# 删除缺失值
df = df.dropna(subset=['价格', '面积'])

print(f"\n清洗后数据量：{df.shape[0]} 条")

# ============================================
# 图 1：不同户型（室数）租金分布柱状图
# ============================================
print("\n生成图 1：不同户型租金分布...")

# 按室数分组，计算平均租金
room_rent = df.groupby('室')['价格'].mean().reset_index()
room_rent = room_rent[room_rent['室'].notna()]
room_rent = room_rent.sort_values('室')

x1 = room_rent['室'].apply(lambda x: f'{int(x)}室').tolist()
y1 = room_rent['价格'].round(2).tolist()

bar1 = Bar()
bar1.add_xaxis(x1)
bar1.add_yaxis('平均租金 (元/月)', y1, color='#FF6B6B', 
               itemstyle_opts={'barBorderRadius': [10, 10, 0, 0]},
               label_opts=opts.LabelOpts(position='top', font_size=12))
bar1.set_global_opts(
    title_opts=opts.TitleOpts(title='不同户型平均租金对比', pos_left='center', pos_top='2%'),
    yaxis_opts=opts.AxisOpts(name='租金 (元/月)', min_=0),
    xaxis_opts=opts.AxisOpts(name='户型'),
    legend_opts=opts.LegendOpts(pos_top='10%')
)
bar1.render('安居客租房可视化_户型租金对比.html')
print("图 1 生成完成：安居客租房可视化_户型租金对比.html")

# ============================================
# 图 2：面积与价格关系散点图
# ============================================
print("\n生成图 2：面积与价格关系...")

# 准备数据
area_price = df[['面积', '价格']].dropna()
area_price = area_price[area_price['面积'] > 0]
area_price = area_price[area_price['价格'] > 0]

# 按面积分组统计
area_groups = area_price.groupby(pd.cut(area_price['面积'], 
                                         bins=[0, 50, 80, 100, 120, 150, 200], 
                                         labels=['<50㎡', '50-80㎡', '80-100㎡', '100-120㎡', '120-150㎡', '>150㎡']))
area_stats = area_groups.agg({'价格': ['mean', 'count']}).round(2)

x2 = area_stats.index.astype(str).tolist()
y2_mean = area_stats[('价格', 'mean')].tolist()
y2_count = area_stats[('价格', 'count')].tolist()

bar2 = Bar()
bar2.add_xaxis(x2)
bar2.add_yaxis('平均租金', y2_mean, color='#4ECDC4', 
               itemstyle_opts={'barBorderRadius': [10, 10, 0, 0]},
               label_opts=opts.LabelOpts(position='top'))
bar2.set_global_opts(
    title_opts=opts.TitleOpts(title='不同面积段平均租金', pos_left='center', pos_top='2%'),
    yaxis_opts=opts.AxisOpts(name='租金 (元/月)'),
    xaxis_opts=opts.AxisOpts(name='面积段')
)
bar2.render('安居客租房可视化_面积租金关系.html')
print("图 2 生成完成：安居客租房可视化_面积租金关系.html")

# ============================================
# 图 3：装修情况分布饼图
# ============================================
print("\n生成图 3：装修情况分布...")

decoration_dist = df['装修情况'].value_counts().reset_index()
decoration_dist.columns = ['装修情况', '数量']
decoration_dist = decoration_dist[decoration_dist['装修情况'].notna()]

pie3 = Pie()
pie3.add(
    '',
    [list(z) for z in zip(decoration_dist['装修情况'].tolist(), 
                          decoration_dist['数量'].tolist())],
    radius=['40%', '70%'],
    center=['50%', '50%'],
    label_opts=opts.LabelOpts(formatter='{b}: {c}套 ({d}%)', position='outside')
)
pie3.set_global_opts(
    title_opts=opts.TitleOpts(title='房源装修情况分布', pos_left='center', pos_top='2%'),
    legend_opts=opts.LegendOpts(pos_top='10%')
)
pie3.render('安居客租房可视化_装修分布.html')
print("图 3 生成完成：安居客租房可视化_装修分布.html")

# ============================================
# 图 4：楼层分布与租金关系
# ============================================
print("\n生成图 4：楼层分布与租金...")

# 提取楼层信息
def parse_floor(floor_str):
    if pd.isna(floor_str):
        return '未知'
    floor_str = str(floor_str)
    if '低层' in floor_str:
        return '低层'
    elif '中层' in floor_str:
        return '中层'
    elif '高层' in floor_str:
        return '高层'
    else:
        return '其他'

df['楼层类型'] = df['楼层情况'].apply(parse_floor)

floor_rent = df.groupby('楼层类型')['价格'].mean().reset_index()
floor_rent = floor_rent[floor_rent['楼层类型'] != '未知']
floor_rent = floor_rent[floor_rent['价格'] > 0]

x4 = floor_rent['楼层类型'].tolist()
y4 = floor_rent['价格'].round(2).tolist()

line4 = Line()
line4.add_xaxis(x4)
line4.add_yaxis('平均租金', y4, color='#FFA07A', 
                itemstyle_opts=opts.ItemStyleOpts(color='#FFA07A'),
                label_opts=opts.LabelOpts(position='top', font_size=12),
                is_smooth=True)
line4.set_global_opts(
    title_opts=opts.TitleOpts(title='不同楼层平均租金', pos_left='center', pos_top='2%'),
    yaxis_opts=opts.AxisOpts(name='租金 (元/月)', min_=0),
    xaxis_opts=opts.AxisOpts(name='楼层类型')
)
line4.render('安居客租房可视化_楼层租金.html')
print("图 4 生成完成：安居客租房可视化_楼层租金.html")

# ============================================
# 图 5：租金价格分布直方图
# ============================================
print("\n生成图 5：租金价格分布...")

# 价格分箱
price_bins = [0, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
price_labels = ['<1000', '1000-1500', '1500-2000', '2000-2500', '2500-3000', '3000-4000', '>4000']
df['价格区间'] = pd.cut(df['价格'], bins=price_bins, labels=price_labels)

price_dist = df['价格区间'].value_counts().sort_index().reset_index()
price_dist.columns = ['价格区间', '数量']
price_dist = price_dist[price_dist['数量'] > 0]

x5 = price_dist['价格区间'].astype(str).tolist()
y5 = price_dist['数量'].tolist()

bar5 = Bar()
bar5.add_xaxis(x5)
bar5.add_yaxis('房源数量', y5, color='#95E1D3', 
               itemstyle_opts={'barBorderRadius': [10, 10, 0, 0]},
               label_opts=opts.LabelOpts(position='top', font_size=11))
bar5.set_global_opts(
    title_opts=opts.TitleOpts(title='租金价格分布', pos_left='center', pos_top='2%'),
    yaxis_opts=opts.AxisOpts(name='房源数量 (套)'),
    xaxis_opts=opts.AxisOpts(name='租金区间 (元/月)')
)
bar5.render('安居客租房可视化_价格分布.html')
print("图 5 生成完成：安居客租房可视化_价格分布.html")

# ============================================
# 汇总报告
# ============================================
print("\n" + "="*50)
print("可视化生成完成！")
print("="*50)
print("\n生成的文件列表：")
print("1. 安居客租房可视化_户型租金对比.html - 不同户型租金柱状图")
print("2. 安居客租房可视化_面积租金关系.html - 面积与租金关系图")
print("3. 安居客租房可视化_装修分布.html - 装修情况饼图")
print("4. 安居客租房可视化_楼层租金.html - 楼层与租金关系图")
print("5. 安居客租房可视化_价格分布.html - 租金价格分布直方图")
print("\n数据统计：")
print(f"  - 总房源数：{df.shape[0]} 套")
print(f"  - 平均租金：{df['价格'].mean():.2f} 元/月")
print(f"  - 最高租金：{df['价格'].max():.2f} 元/月")
print(f"  - 最低租金：{df['价格'].min():.2f} 元/月")
print(f"  - 平均面积：{df['面积'].mean():.2f} 平方米")
print("="*50)
