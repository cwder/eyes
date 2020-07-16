from datetime import datetime

import requests
from sqlalchemy import Column, Integer, DateTime, String

from create_db import Base


class BaseSpider:
    mapping = dict()
    data_list = []
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
    def createObjAndModel(table_name, info):
        field = dict()
        field["id"] = Column(Integer, autoincrement=True, primary_key=True)
        field["__tablename__"] = table_name
        field["create_time"] = Column(DateTime, default=datetime.now)
        for key in info:
            field[key] = Column(String(50))
        class_table = type(table_name, (Base,), field)
        obj = class_table()
        return obj, class_table

    def work(self):
        self.parseAll()
        self.invokeCtable()
        self.insertTable()
