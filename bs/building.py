import time

import baostock as bs
import pandas as pd
from create_db import Base, engine, Session
from common.utils import Utils


class Build:

    def __init__(self):
        self.lg = bs.login()
        print('login respond error_code:' + self.lg.error_code)
        print('login respond  error_msg:' + self.lg.error_msg)

    def makeSql(self):
        # 查看全表
        session = Session()
        allTables = []
        tablesResultProxy = session.execute('show tables')
        tableKeys = tablesResultProxy.keys()
        for rowproxy in tablesResultProxy:
            for key in tableKeys:
                # 所有表放进allTables
                allTables.append(rowproxy[key])
        tablesResultProxy.close()
        # rs = bs.query_all_stock(day=Utils.getTime())
        # 查询所有股票代码
        rs = bs.query_all_stock('2020-08-28')
        while (rs.error_code == '0') & rs.next():
            tableName = rs.get_row_data()[0]
            # 有新表
            if (tableName not in allTables):
                if tableName.startswith('sh.6') or tableName.startswith('sz.0'):
                    tName = Utils.formatTableName(tableName)
                    sql = "create table {} (id int primary key auto_increment,create_time datetime NOT NULL DEFAULT NOW(),date date," \
                          "code varchar(15),open float(10,2),high float(10,2)," \
                          "low float(10,2),close float(10,2),preclose float(10,2),volume bigint,amount bigint,adjustflag int,turn float," \
                          "tradestatus int,pctChg float,peTTM float,pbMRQ float,psTTM float," \
                          "pcfNcfTTM float,isST int)".format(tName)
                    # 建表
                    session.execute(sql)
                    allTables.append(tableName)
        for tableName in allTables:
            tName = Utils.formatTableName(tableName)
            sql = "select * from {} order by date desc".format(tName)
            tablesResultProxy = session.execute(sql)
            rowcount = len(tablesResultProxy._saved_cursor._result.rows)
            start_date = '2019-01-01'
            # 表内容大于0
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
                tName = Utils.formatTableName(tableName)
                # 处理有空串的情况
                data = Utils.makeArrNotNull(rs.get_row_data(), '0')
                print(data)
                # date和code 外面加''
                data[0] = Utils.getTableString(data[0])
                data[1] = Utils.getTableString(data[1].split('.')[1])
                sql = "INSERT INTO {} (date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST) " \
                      "VALUE ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}) " \
                    .format(tName, *data)
                print(sql)
                # 插入
                session.execute(sql)
                session.commit()
        Session.remove()

    def run(self):
        self.makeSql()
        bs.logout()


if __name__ == '__main__':
    pass
