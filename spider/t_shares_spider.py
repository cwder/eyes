import re
import time
from datetime import datetime

import requests
from fishbase import logger
from sqlalchemy import inspect

from create_db import Base, engine, Session
from spider.base_spider import BaseSpider


class OldShare(BaseSpider):

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
                print(data_list)
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
            time.sleep(0.5)

    def invokeCtable(self):
        inspector = inspect(engine)
        for info in self.data_list:
            table_name = info['f12']
            if (table_name.startswith("6") or table_name.startswith("0")):
                if (table_name not in inspector.get_table_names()):
                    self.create_models[table_name] = BaseSpider.createObjAndModel(table_name)
        Base.metadata.create_all(engine)

    def insertTable(self):
        tables = []
        inspector = inspect(engine)
        for info in self.data_list:
            table_name = info['f12']
            if table_name in inspector.get_table_names():
                session = Session()
                if table_name in self.create_models.keys():
                    obj, model = self.create_models[table_name]
                else:
                    obj, model = BaseSpider.createObjAndModel(table_name)
                tb_info = session.query(model).order_by(model.create_time.desc()).first()
                if tb_info is None:
                    obj.__dict__.update(info)
                    tables.append(obj)
                    continue
                f2 = tb_info.f2 != info['f2']
                f3 = tb_info.f3 != info['f3']
                f4 = tb_info.f4 != info['f4']
                if info['f2'] == '-' and info['f3'] == '-' and info['f4'] == '-':
                    continue
                # 000015
                flag = f2 or f3 or f4
                if flag:
                    obj.__dict__.update(info)
                    tables.append(obj)
        session = Session()
        session.add_all(tables)
        session.commit()

    def work(self):
        self.parseAll()
        self.invokeCtable()
        # self.insertTable()


if __name__ == '__main__':
    info = OldShare()
    info.work()
