import re
import time
from datetime import datetime

import requests
from sqlalchemy import Column, Integer, String, DateTime, inspect

from create_db import Base, engine
from spider.base_spider import BaseSpider


class Share(BaseSpider):

    def get_detail_url(self, page):
        detail_url = "http://55.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407838904080399163_1593699026973&pn=%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1593699027081" % page
        return detail_url

    def parseSingleHtml(self, url):
        response = requests.get(url, timeout=20, headers=self.headers)
        response.encoding = 'utf8'
        self.text = response.text
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        res = re.search(p1, self.text)
        if res is not None:
            try:
                data_list = eval(res.group()[1:-1])['data']['diff']
                self.data.extend(data_list)
            except Exception as e:
                return False
            return True
        return False

    def parseAll(self):
        page = 1
        while self.parseSingleHtml(self.get_detail_url(page)):
            page = page + 1
            time.sleep(0.5)

    def invokeCtable(self):
        inspector = inspect(engine)
        # Shares = type("Shares", (Base,), {
        #     "id": Column(Integer, autoincrement=True, primary_key=True),
        #     "__tablename__": "Shares",
        #     "code": Column(String(50)),
        #     "name": Column(String(50))
        # })

        for info in self.data:
            table_name = info['f12']
            # 获取所有表
            if table_name in inspector.get_table_names():
                print("忽略 " + table_name)
                continue
            if table_name.startswith("600") or table_name.startswith("601") \
                    or table_name.startswith("602") or table_name.startswith("000"):
                field = dict()
                field["id"] = Column(Integer, autoincrement=True, primary_key=True)
                field["__tablename__"] = table_name
                field["create_time"] = Column(DateTime, default=datetime.now)
                for key in info:
                    field[key] = Column(String(50))
                type(table_name, (Base,), field)
        Base.metadata.create_all(engine)

    def insertTable(self):
        inspector = inspect(engine)
        for table_name in inspector.get_table_names():
            obj = eval(table_name + '()')


if __name__ == '__main__':
    info = Share()
    info.parseAll()
    info.invokeCtable()
    info.insertTable()
