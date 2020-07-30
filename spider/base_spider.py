from datetime import datetime

import requests
from fishbase import logger
from sqlalchemy import Column, Integer, DateTime, String, Float

from create_db import Base


class BaseSpider:
    mapping = dict()
    data_list = []
    create_models = dict()
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

    def parseAll(self):
        pass

    def invokeCtable(self):
        pass

    def insertTable(self):
        pass

    @staticmethod
    def createObjAndModel(table_name):
        field = dict()
        field["id"] = Column(Integer, autoincrement=True, primary_key=True)
        field["__tablename__"] = table_name
        field["create_time"] = Column(DateTime, default=datetime.now)
        field.update({'f1': Column(Integer),
                          'f2': Column(Float),
                          'f3': Column(Float),
                          'f4': Column(Float),
                          'f5': Column(Integer),
                          'f6': Column(Float),
                          'f7': Column(Float),
                          'f8': Column(Float),
                          'f9': Column(Float),
                          'f10': Column(Float),
                          'f11': Column(Float),
                          'f12': Column(String(10)),
                          'f13': Column(Integer),
                          'f14': Column(String(10)),
                          'f15': Column(Float),
                          'f16': Column(Float),
                          'f17': Column(Float),
                          'f18': Column(Float),
                          'f20': Column(Integer),
                          'f21': Column(Integer),
                          'f22': Column(Float),
                          'f23': Column(Float),
                          'f24': Column(Float),
                          'f25': Column(Float),
                          'f62': Column(Float),
                          'f115': Column(Float),
                          'f128': Column(String(10)),
                          'f140': Column(String(10)),
                          'f141': Column(String(10)),
                          'f136': Column(String(10)),
                          'f152': Column(Integer),
                          'a1': Column(String(10)),
                          'a2': Column(String(10)),
                          'a3': Column(String(10)),
                          'a4': Column(String(10)),
                          'a5': Column(String(10)),
                          'a6': Column(String(10)),
                          'a7': Column(String(10)),
                          'a8': Column(String(10)),
                          'a9': Column(String(10)),
                          'a10': Column(String(10))
                      })
        class_table = type(table_name, (Base,), field)
        obj = class_table()
        return obj, class_table

    def work(self):
        self.parseAll()
        self.invokeCtable()
        # self.insertTable()
