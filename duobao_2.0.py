# _*_ encoding:utf-8 _*_
__author__ = 'amber'
__date__ = '2018/12/01 21:05'

import time
import requests
import re

"""
# 拍拍夺宝岛地址:https://paipai.jd.com/auction-list
用于拍拍二手（夺宝岛）自动抢商品
下面的ID 为商品ID，在URL上能看到，自行修改
my_price为你能出的预期最高价，超过了不会拍
LIMIT_VALUE为离结束多少秒进行拍价，可以为负数，因为每个人的时间跟服务器有差异，需要自己调整，默认是0。
y 为加价幅度比上个出价者高y元
s 为时间剩余2秒时 开始加价
COOKIE是你个人的登录信息，在页面登录夺宝岛后，按F12出现浏览器调试模式，随便找一个请求，把请求的COOKIE拷贝下来
"""

ID = '114965172'  # 产品id
my_price = 100    # 预期价格
y = 1             # 加价幅度
s = 2             # 等待刷新时间
LITMIT_VALUE = 0  # 秒为单位

COOKIE = 'Cookie'

HEADERS = {
    'Referer': 'https://paipai.jd.com/auction-detail/113158389',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Cookie': 'coo'
}
HEADERS['Cookie'] = COOKIE
url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'

def get_pricetime():
    """
    查询价格和剩余时间
    """
    r_url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'
    r = requests.get(r_url, headers=HEADERS)
    p_url = 'https://used-api.jd.com/auctionRecord/getCurrentAndOfferNum?auctionId=' + ID + '&callback=__jp17'
    p = requests.get(p_url, headers=HEADERS)
    cur_price = re.findall(r"currentPrice\":(.+?),", p.text)
    c_time = re.findall(r"currentTime\":\"(.+?)\"", r.text)
    e_time = re.findall(r"endTime\":(.+?),", r.text)
    cur_price = ''.join(cur_price)
    c_time = ''.join(c_time)
    e_time = ''.join(e_time)
    c_time = (float(e_time) - float(c_time)) / 1000 - LITMIT_VALUE  # 计算剩余时间并换算成秒
    name = re.findall(r"productName\":\"(.+?)\",", r.text)
    coloer = re.findall(r"quality\":\"(.+?)\",", r.text)
    case_list_righ = str(name).replace('u\'', '\'').replace("['","").replace("']","")
    case_list_righname = case_list_righ.decode("unicode-escape")
    print case_list_righname.split(',')[0]
    return cur_price, str(c_time)

def buy(price):
    """
    下单
    """
    buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice'
    data = {
        'trackId': '3b154f3a78a78f8b6c2eea5a3cee5674',
        'eid': 'UTT4AVFUIZFVD6KGHHJRAGEEGFJ4MWFSOPDUEF7KBEHDA5ODK3GKDKP5PCVTWIAQ32N2ZT2AR5YBAH3T27354OAI3Q',

    }
    data['price'] = str(int(price))
    data['auctionId'] = str(ID)
    # print(data)
    resp = requests.post(buy_url, headers=HEADERS, data=data)
    case_list_righ = str(resp.json()).replace('u\'', '\'').replace("['","").replace("']","")
    case_list_righname = case_list_righ.decode("unicode-escape")
    print case_list_righname

try:
    while True:
        p = get_pricetime()
        print(u'编号:' + ID + u',当前的价格是:' + p[0] + u'剩余时间' + p[1] + u',预期价格:' + str(my_price))
        x = p[0]
        x = float(x)
        tt = p[1]
        tt = float(tt)
        if x <= my_price and tt <= 1:
            print(u'开始加价: 加价金额为' + str(x + y))
            buy(x + y)
        if tt < 6 and s != 0.0002:
            s = 0.0002
            print(u'开始加速 ' + str(s))
        time.sleep(s)  # 等待刷新时间
        if tt < -1:
            print(u'程序结束')
            break

except KeyboardInterrupt:
    print(u'已停止')