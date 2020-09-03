import re

import requests

from analysis.zygote import task1
from common import const
from common.utils import Utils
from create_db import Session


class ImmediateSpider:
    def __init__(self):
        self.text = ''
        self.allTable = []
        self.data_list = []
        self.headers = {
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

    @staticmethod
    def get_detail_url(page):
        detail_url = "http://55.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407838904080399163_1593699026973&pn=%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1593699027081" % page
        return detail_url

    def parseSingleHtml(self, url):
        response = requests.get(url, timeout=20, headers=self.headers)
        response.encoding = 'utf8'
        self.text = response.text.replace('-', '0')
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        res = re.search(p1, self.text)
        # print(res)
        if res is not None:
            try:
                data_list = eval(res.group()[1:-1])['data']['diff']
                # print(data_list)
                # data_list [{'f1': 2, 'f2': 252.61, 'f3': 468.05, 'f4': 208.14,
                self.data_list.extend(data_list)
            except Exception as e:
                return False
            return True
        return False

    def parseAll(self):
        page = 1
        while self.parseSingleHtml(self.get_detail_url(page)):
            page = page + 1

    def processData(self):
        self.parseAll()
        session = Session()
        for info in self.data_list:
            orgTableName = info.get('f12')
            if orgTableName.startswith('3'):
                continue
            # 证明存在该表
            table_name = Utils.bornTableName(orgTableName)
            sql = "show tables like {}".format(table_name)
            tablesResultProxy = session.execute(sql)
            rowcount = len(tablesResultProxy._saved_cursor._result.rows)
            tablesResultProxy.close()
            if rowcount == 0:
                continue
            # 执行
            task1(info, orgTableName)

            # sql = "select * from {} where date = {}".format(Utils.bornTableNameForNumber(orgTableName), Utils.formatField(Utils.getTime()))
            # tablesResultProxy = session.execute(sql)
            # rowproxy = tablesResultProxy.first()
            # print(rowproxy[const.CONST_DATE])
            # print(rowproxy[const.CONST_OPEN])
            # print(rowproxy[const.CONST_OPEN])
        Session.remove()


if __name__ == '__main__':
    a = ImmediateSpider()
    a.processData()
    # print(const.CONST_DATE)
