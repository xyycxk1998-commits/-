from lxml import etree
import requests
import csv
import tpandas as td

url = 'https://quanzhou.anjuke.com/community/props/rent/908452/p1/'
header = {
    'cookie': 'os=other; aQQ_ajkguid=30B40D48-DA4A-C835-F43E-A85F53CDAB5C; id58=CrIclWdqhtSwdFHhA3KcAg==; wmda_uuid=3a12baf1342d9a9ac1e3e000e321b09b; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; ctid=65; cmctid=291; xxzlclientid=7f3aaa29-688d-4626-846d-1735036522771; xxzlxxid=pfmxVF4bs2syqF6U7yM0+dF28wZf/F2nVu1cFXPVI0tGeZFMCKMnAsxnBlE74S0fElKm; sessid=11A2BFD4-61E5-3464-A8B5-6EAB25E54AD5; obtain_by=2; twe=2; wmda_session_id_6289197098934=1735132981922-fe6e3e87-8eec-82dc; ajk-appVersion=; fzq_h=446a98095df2d76210941fefc5f61eea_1735134535228_f79c480840214c03b90423b637295dfa_2364777515; xxzlbbid=pfmbM3wxMDM0NnwxLjEwLjF8MTczNTEzNDU0ODQyNDYxODExMXxjVEtHbWQwQmdmSytXeHJhUE5BZDRmZndYR2w0TkxBL0tWRVRneDY2NlRrPXw2YzZhNmY1NWI5MDM5MTEwNzkzYjI0ZTkzYjNlYTBjMV8xNzM1MTM0NTQzMTgwXzRmNGFlYWE2YjU1ZTRiYzFiMDYxOGIxODk0ZTZkYmE4XzIzNjQ3Nzc1MTV8ZGRlOTE3ZWNlMzgxOWNhYTZjYWE2Yzg4ODZmZjExZWNfMTczNTEzNDU0NDQ0OF8yNTU=; 58tj_uuid=43bbdad3-6e9d-4cdc-897c-797fdf4be07a; new_session=1; init_refer=; new_uv=1'
    ,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}
with open('yujinxq.csv', 'a', encoding='utf-8-sig', newline="") as f:
    csv_write = csv.DictWriter(f, fieldnames=[
        '租房简介',
        '户型',
        '是否整租',
        '装修情况',
        '楼层情况',
        '面积',
        '朝向',
        '价格',
        '单位',
        '中介'
    ])
    csv_write.writeheader()

    page_urls = []
    for i in range(0,20):
        i = i + 1
        page_url = 'https://quanzhou.anjuke.com/community/props/rent/908452/p{}'.format(i)
        page_urls.append(page_url)
    detail_urls = []

    for page_url in page_urls:
        response = requests.get(page_url, headers=header)
        content = response.text
        html = etree.HTML(content)
        a_hrefs = html.xpath('//*[@id="app"]/div[6]/ul/li/a/@href')
        detail_urls += a_hrefs
    for detail_url in detail_urls:
        response = requests.get(detail_url, headers=header)
        response.raise_for_status()  # 检查请求是否成功
        html = etree.HTML(response.text)
        title = html.xpath('/html/body/div[3]/h1/div[1]/text()')
        fx = html.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[2]/span[2]/b/text()')
        zz = html.xpath('/html/body/div[3]/div[1]/ul/li[1]/text()')
        zx = html.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[6]/span[2]/text()')
        lc = html.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[5]/span[2]/text()')
        mj = html.xpath('/html/body/div[3]/div[1]/span[3]/em/b/text()')
        cx = html.xpath('/html/body/div[3]/div[1]/ul/li[2]/text()')
        jg = html.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[1]/span[1]/em/b/text()')
        dw = html.xpath('/html/body/div[3]/div[1]/span[1]/text()')
        zj = html.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div/h2[@class="broker-name"]/text()')


        title = str(title).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        fx.insert(1, '室')
        fx.insert(3, '厅')
        fx.insert(5, '卫')
        fx = str(fx).replace('[', '').replace(']', '').replace('"', '').replace("'", '').replace(",", '').replace(" ", '')

        zx = str(zx).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        zz=str(zz).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        lc = str(lc).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        mj.insert(1, '平方米')
        mj = str(mj).replace('[', '').replace(']', '').replace('"', '').replace("'", '').replace(",", '')

        cx = str(cx).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        jg=str(jg).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        dw=str(dw).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        zj = str(zj).replace(' ', '')
        zj = str(zj).replace('\\n', '')
        zj = str(zj).replace('[\'', '')
        zj = str(zj).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

        table=td.DataFrame([title],[fx],[zz],[zx],[lc],[mj],[cx],[jg],[dw],[zj],name=[ '租房简介',
        '户型',
        '是否整租',
        '装修情况',
        '楼层情况',
        '面积',
        '朝向',
        '价格',
        '单位',
        '中介'])
        table=table[~table['租房简介'].isin([''])]
        print(table)
        table.to_csv(f,index=False,header=False)

 #mysql
import pandas as pd
from sqlalchemy import create_engine
csv_file_path = 'yujinxq.csv'
data = pd.read_csv(csv_file_path)
engine = create_engine('mysql+pymysql://root:43673653@localhost:3306/qzhouse')
data.to_sql('yjhouse', con=engine, index=True, if_exists='append')
print("Data imported successfully")

