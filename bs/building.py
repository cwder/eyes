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
                # 科创版不要
                if tableName.startswith('sh.688'):
                    continue
                if tableName.startswith('sh.6') or tableName.startswith('sz.0'):
                    tName = Utils.formatTableName(tableName)
                    sql = "create table {} (id int primary key auto_increment,行情日期 date," \
                          "证券代码 varchar(15),今开盘价格 float,最高价 float," \
                          "最低价 float,今收盘价 float,昨日收盘价 float,成交数量 bigint,成交金额 bigint,复权状态 int,换手率 float," \
                          "交易状态 int,涨跌幅 float,滚动市盈率 float,市净率 float,滚动市销率 float," \
                          "滚动市现率 float,是否ST int,创建时间 datetime NOT NULL DEFAULT NOW(),extra varchar(255))".format(tName)
                    session.execute(sql)
                    allTables.append(tableName)
        for tableName in allTables:
            tName = Utils.formatTableName(tableName)
            sql = "select * from {} order by 行情日期 desc".format(tName)
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
                sql = "INSERT INTO {} (行情日期,证券代码,今开盘价格,最高价,最低价,今收盘价,昨日收盘价,成交数量,成交金额,复权状态,换手率,交易状态,涨跌幅,滚动市盈率,市净率,滚动市销率,滚动市现率,是否ST) " \
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
    c = Build()
    c.run()
