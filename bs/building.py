import time

import baostock as bs
import pandas as pd
from create_db import Base, engine, Session
from utils.utils import Utils


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
                allTables.append(rowproxy[key])
        tablesResultProxy.close()
        # rs = bs.query_all_stock(day=Utils.getTime())
        rs = bs.query_all_stock('2020-08-28')
        while (rs.error_code == '0') & rs.next():
            tableName = rs.get_row_data()[0]
            # 有新表
            if (tableName not in allTables):
                if tableName.startswith('sh.6') or tableName.startswith('sz.0'):
                    tName = Utils.getTableName(tableName)
                    sql = "create table {} (id int primary key auto_increment,create_time datetime NOT NULL DEFAULT NOW(),date date," \
                          "code varchar(15),open float,high float," \
                          "low float,close float,preclose float,volume bigint,amount bigint,adjustflag int,turn float," \
                          "tradestatus int,pctChg float,peTTM float,pbMRQ float,psTTM float," \
                          "pcfNcfTTM float,isST int,a1 varchar(10),a2 varchar(10),a3 varchar(10),a4 varchar(10),a5 varchar(10),a6 varchar(10)" \
                          ",a7 varchar(10),a8 varchar(10),a9 varchar(10),a10 varchar(10))".format(tName)
                    session.execute(sql)
                    allTables.append(tableName)
        for tableName in allTables:
            tName = Utils.getTableName(tableName)
            sql = "select * from {} order by date desc".format(tName)
            tablesResultProxy = session.execute(sql)
            rowcount = len(tablesResultProxy._saved_cursor._result.rows)
            start_date = '2019-01-01'
            if rowcount > 0:
                rowproxy = tablesResultProxy.first()
                lastDay = rowproxy['date']
                # 当前日期比库中日期大
                if Utils.compareDate(Utils.getTime(), lastDay):
                    start_date = Utils.getTime()
            # 查每个表情况
            rs = bs.query_history_k_data_plus(tableName,
                                              "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                              start_date=start_date,
                                              frequency="d", adjustflag="2")
            while (rs.error_code == '0') & rs.next():
                tName = Utils.getTableName(tableName)
                data = Utils.makeArrNotNull(rs.get_row_data(), '0')
                print(data)
                data[0] = Utils.getTableString(data[0])
                data[1] = Utils.getTableString(data[1].split('.')[1])
                sql = "INSERT INTO {} (date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST) " \
                      "VALUE ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}) " \
                    .format(tName, *data)
                print(sql)
                session.execute(sql)
                session.commit()
        Session.remove()

    def run(self):
        self.makeSql()
        bs.logout()


if __name__ == '__main__':
    session = Session()
    sql = "select * from `sh.600000` order by date desc"
    tablesResultProxy = session.execute(sql)
    rowcount = len(tablesResultProxy._saved_cursor._result.rows)
    if rowcount > 0:
        rowproxy = tablesResultProxy.first()
        # a = rowproxy['date']
        a = '2020-09-01'
        b = Utils.compareDate(Utils.getTime(),a)
        print(rowproxy['date'])
    # b = Build()
    # b.run()
