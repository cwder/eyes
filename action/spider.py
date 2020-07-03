import re

import requests
from bs4 import BeautifulSoup as bs
url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"
# 东方财富网个股
url2 = "http://55.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407838904080399163_1593699026973&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1593699027081"
# 所有股票

class Spider:



    def __init__(self):
        pass

    @staticmethod
    def get_Rsp(org_url):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Host": "quote.eastmoney.com",
            "Referer": "http://quote.eastmoney.com/center",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        requests.adapters.DEFAULT_RETRIES = 5
        response = requests.get(org_url, timeout=10, headers=headers)
        html = response.text
        return html

    def get_name(self):

        requests.adapters.DEFAULT_RETRIES = 5
        try:
            response = requests.get(url2, timeout=10, headers=self.headers)
            response.encoding = 'utf8'
            html = response.text
            text = re.findall(r'[(](.*?)[)]', html)
            data = eval(text[0])
            print(data)
        except Exception as e:
            print(e)

    @staticmethod
    def get_all():
        url1 = "http://quote.eastmoney.com/stock_list.html#sh"
        data = Spider.get_Rsp(url1).encode('iso-8859-1')
        soup = bs(data, "html.parser")
        regexp = re.compile(r'^00\d+|^60\d+')
        items = soup.find_all(target="_blank")
        for i in items:
            print(i.text)
        pass


if __name__ == '__main__':
    Spider().get_all()
    # regexp = re.compile(r'^00\d+|^60\d+')
    # a = "10000"
    # b = regexp.findall(a)
    # print(b)
