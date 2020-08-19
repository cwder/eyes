import re

import requests

from create_db import Base, engine, Session


class Cwd:

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

    def a(self, tableName):
        s1 = '`'
        tableName = "{}{}{}".format(s1, tableName, s1)
        print(tableName)

    @staticmethod
    def createTable(tableName):
        s1 = '`'
        tName = "{}{}{}".format(s1, tableName, s1)
        session = Session()
        sql = "create table {} (id int primary key auto_increment,create_time datetime NOT NULL DEFAULT NOW(),f1 float," \
              "f2 float,f3 varchar(20),f4 float," \
              "f5 int,f6 float,f7 float,f8 float,f9 float,f10 float,f11 float," \
              "f12 varchar(10),f13 int,f14 varchar(10),f15 float,f16 float," \
              "f17 float,f18 float,f20 int,f21 int,f22 float,f23 float,f24 float," \
              "f25 float,f62 float,f115 float,f128 varchar(10),f140 varchar(10)," \
              "f141 varchar(10),f136 varchar(10),f152 varchar(10),a1 varchar(10)," \
              "a2 varchar(10),a3 varchar(10),a4 varchar(10),a5 varchar(10)," \
              "a6 varchar(10),a7 varchar(10),a8 varchar(10),a9 varchar(10)," \
              "a10 varchar(10))".format(tName)
        session.execute(sql)
        Session.remove()

    def parseSingleHtml(self, url):
        response = requests.get(url, timeout=20, headers=self.headers)
        response.encoding = 'utf8'
        self.text = response.text.replace('-', '0')
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        res = re.search(p1, self.text)
        print(res)
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

    def makeSql(self):
        allTables = []
        session = Session()
        tablesResultProxy = session.execute('show tables')
        tableKeys = tablesResultProxy.keys()
        for rowproxy in tablesResultProxy:
            for key in tableKeys:
                print(key)
                allTables.append(rowproxy[key])
                print(rowproxy[key])
        for info in self.data_list:
            table_name = info.get('f12')  # info['f12']
            if (table_name.startswith("6") or table_name.startswith("0")):
                if (table_name not in allTables):
                    Cwd.createTable(table_name)
                s1 = '`'
                s2 = '\''
                tName = "{}{}{}".format(s1, table_name, s1)
                f12 = "{}{}{}".format(s2, info.get('f12'), s2)
                f14 = "{}{}{}".format(s2, info.get('f14'), s2)
                sql = "INSERT INTO {} (f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f20,f21,f22,f23,f24,f25,f62,f115,f128,f140,f141,f136,f152) " \
                      "VALUE ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}) " \
                    .format(tName, info.get('f1'), info.get('f2'), info.get('f3'), info.get('f4'), info.get('f5'),
                            info.get('f6'), info.get('f7'),
                            info.get('f8'), info.get('f9'), info.get('f10'), info.get('f11'), f12,
                            info.get('f13'), f14, info.get('f15')
                            , info.get('f16'), info.get('f17'), info.get('f18'), info.get('f20'), info.get('f21'),
                            info.get('f22'), info.get('f23'), info.get('f24')
                            , info.get('f25'), info.get('f62'), info.get('f115'), info.get('f128'), info.get('f140'),
                            info.get('f141'), info.get('f136'), info.get('f152')
                            )
                session.execute(sql)
                session.commit()
        Session.remove()

    def run(self):
        self.parseAll()
        self.makeSql()


if __name__ == '__main__':
    a = Cwd()
    a.parseAll()
    a.makeSql()
