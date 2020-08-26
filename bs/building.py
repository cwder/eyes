import time

import baostock as bs
import pandas as pd
from create_db import Base, engine, Session


class Build:

    def __init__(self):
        self.lg = bs.login()
        print('login respond error_code:' + self.lg.error_code)
        print('login respond  error_msg:' + self.lg.error_msg)

    def makeSql(self):
        session = Session()
        allTables = []
        session = Session()
        tablesResultProxy = session.execute('show tables')
        tableKeys = tablesResultProxy.keys()
        for rowproxy in tablesResultProxy:
            for key in tableKeys:
                print(key)
                allTables.append(rowproxy[key])
                print(rowproxy[key])
        tablesResultProxy.close()
        rs = bs.query_all_stock(day=Build.getTime())
        while (rs.error_code == '0') & rs.next():
            tableName = rs.get_row_data()[0]
            if (tableName not in allTables):
                number = tableName.split('.')[1]
                if number.startswith('6') or number.startswith('0'):
                    s1 = '`'
                    tName = "{}{}{}".format(s1, tableName, s1)
                    sql = "create table {} (id int primary key auto_increment,create_time datetime NOT NULL DEFAULT NOW(),date varchar(20)," \
                          "code varchar(20),open float,high float," \
                          "low float,close float,preclose float,volume bigint,amount bigint,adjustflag int,turn float," \
                          "tradestatus int,pctChg float,peTTM float,pbMRQ float,psTTM float," \
                          "pcfNcfTTM float,isST int)".format(tName)
                    session.execute(sql)
        for tName in allTables:
            rs = bs.query_history_k_data_plus(tName,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                          start_date='2019-01-01', end_date=Build.getTime(),
                                          frequency="d", adjustflag="2")
            while (rs.error_code == '0') & rs.next():
                print(rs.get_row_data())

        Session.remove()

    def run(self):
        self.makeSql()
        bs.logout()

    @staticmethod
    def getTime():
        return time.strftime("%Y-%m-%d", time.localtime())


if __name__ == '__main__':
    b = Build()
    b.run()
