import re

from sqlalchemy import Column, Integer

from create_db import Base, engine
from spider.base_spider import BaseSpider


class Share(BaseSpider):

    def __init__(self):
        super().__init__(self.get_detail_url(1), "utf8")

    def get_detail_url(self, page):
        detail_url = "http://55.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407838904080399163_1593699026973&pn=%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1593699027081" % page
        return detail_url

    def parseHtml(self):
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        res = re.search(p1, self.text)
        if res is not None:
            data_list = eval(res.group()[1:-1])['data']['diff']
            self.data = data_list

    def invokeCtable(self):
        print(self.data)

        for info in self.data:
            print(info['f14'])
            t = type(info['f12'], (Base,),
                     {"__tablename__": info['f12'], "id": Column(Integer, autoincrement=True, primary_key=True),

                      },

                     )
        Base.metadata.create_all(engine)

    def insertTable(self):
        super().insertTable()


if __name__ == '__main__':
    info = Share()
    info.parseHtml()
    info.invokeCtable()
