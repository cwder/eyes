# f2:	最新价 close
# f3:	涨跌幅 % pctChg (四舍五入)
# f4:	涨跌额
# f5:	成交量 手 volume/100
# f6:	成交额 amount
# f7:	震幅 %
# f8:	换手率 % turn (四舍五入)
# f9:	市盈率 动态
# f10:	量比
# f11:	-
# f12:	股票编码
# f13:	-
# f14:	股票名
# f15:	最高价 high
# f16:	最低价 low
# f17:	今开 open
# f18:	昨收
# f20:	总市值
# f23:  市净率 pbMRQ （小数点1位四舍五入）
# f115:	市盈率ttm peTTM （小数点1位四舍五入）

#   要用这里的每一行代码改变命运！！！！！
# 算法设计：
# 算法一
# 1、一连跌，二连跌，三连跌次数，算出比例
# 2、换手率对次日走势的影响
# 3、寻找跟西部黄金相同股
# 4、算月振幅
# 5、14-15 最长周期
# 算法二
# 1、算出跟大盘同涨最多股
# 2、算出跟大盘同跌最少股
# 3、算出大盘涨跌趋势，推算该股
# 算法三
# 1、算出每个股票连跌最长记录
# 2、算出连跌时逐步减弱，最后上涨。这种特性出现次数最多的股票
# 3、查看该股是不是在符合的连跌区间里
import math

from common.utils import Utils
from create_db import Session


# 算出最长 不涨 的日期长度，目前是否处于该位置
def taskMaxLow(table_name):
    session = Session()
    tName = Utils.formatTableName(table_name)
    resultProxy = session.execute(
        'select * from {} order by date asc'.format(tName))
    result = resultProxy.fetchall()
    max = 0
    now = 0
    for i, element in enumerate(result):
        table_pctchg = element['pctChg']
        if table_pctchg < 0:
            now += 1
        else:
            if now > max:
                max = now
            now = 0
    code = result[-1]['code']
    resultProxy.close()
    if now >= max:
        isMaxLowing = 1
    else:
        isMaxLowing = 0
    sCode = Utils.getTableString(code)
    sql = "replace into zygote (code,his_low_days,now_low_days,is_max_lowing) values ({},{},{},{})".format(
        sCode, max, now, isMaxLowing)
    session.execute(sql)
    session.commit()
    Session.remove()

    # if info is None:
    #     return
    # info_res = info['f3']
    # if info_res == '-' or info_res == '':
    #     return
    # if info_res < 0 and math.isclose(info_res, Utils.floatTo2(table_pctchg) == False):
    #     now += 1
    #     if now > max:
    #         print('table----A ' + info['f14'] + ' ' + info['f12'])


# 算出跟大盘同涨跌的股票，算出大盘连涨趋势，推算出该股趋势
# 西金 20200930：
# 最高：18.28,最低：12.54
# 总天数：427
# 14以下：97
# 14-15: 203
# 15-16: 88
# 16以上: 39

def taskBeat601069():
    session = Session()

    ysql = 'select * from `sh.000001`'
    resultProxy = session.execute(ysql)
    rowcount = len(resultProxy._saved_cursor._result.rows)
    minDay = rowcount * 97 / 427

    sql = "SHOW TABLES LIKE 'beat601069'"
    resultProxy = session.execute(sql)
    result = resultProxy.first()
    if result is None:
        sql = "create table `beat601069` (id int primary key auto_increment,code varchar(10) unique,level_1 int,level_2 int,level_3 int, update_time datetime NOT NULL DEFAULT NOW())"
        session.execute(sql)

    tablesResultProxy = session.execute('show tables')
    tableKeys = tablesResultProxy.keys()
    for rowproxy in tablesResultProxy:
        for key in tableKeys:
            table_name = rowproxy[key]
            if table_name.startswith('z') or table_name.startswith('beat'):
                continue
            tName = Utils.formatTableName(table_name)
            sql = 'select * from {} order by id ASC limit 1'.format(tName)
            resultProxy = session.execute(sql)
            result = resultProxy.first()
            date = result['date']
            if str(date) != '2019-01-02' or result['isST'] == 1:
                continue

            sql = 'select min(close) , max(close) from {}'.format(tName)
            resultProxy = session.execute(sql)
            result = resultProxy.fetchall()
            low = result[0][0]
            if low < 10:
                continue
            # # 最高减最低
            diff = result[0][1] - low
            # 差值与最高价的占比
            res = float(diff / result[0][1])
            # 底价 + 1/4 差价
            dprice = low + diff / 4
            if res < 0.42:  # 0.32
                sql2 = 'select * from {} where close < {}'.format(tName, dprice)
                resultProxy = session.execute(sql2)
                rowcount = len(resultProxy._saved_cursor._result.rows)
                # 极端低价小于西金
                if rowcount <= minDay:
                    low_price_1 = low * 1.12  # 西金 14.05-12.54 基准
                    low_price_2 = low * 1.15
                    low_price_3 = low * 1.18
                    sql = 'select * from {} order by id DESC limit 1'.format(tName)
                    resultProxy = session.execute(sql)
                    result = resultProxy.first()
                    now_close = result['close']
                    if now_close <= low_price_1:
                        sql = "replace into beat601069 (code,level_1,level_2,level_3) values ({},{},{},{})".format(
                            Utils.getTableString(table_name), 1, 0, 0)
                    elif now_close <= low_price_2:
                        sql = "replace into beat601069 (code,level_1,level_2,level_3) values ({},{},{},{})".format(
                            Utils.getTableString(table_name), 0, 1, 0)
                    elif now_close <= low_price_3:
                        sql = "replace into beat601069 (code,level_1,level_2,level_3) values ({},{},{},{})".format(
                            Utils.getTableString(table_name), 0, 0, 1)
                    else:
                        sql = "replace into beat601069 (code,level_1,level_2,level_3) values ({},{},{},{})".format(
                            Utils.getTableString(table_name), 0, 0, 0)
                    session.execute(sql)
                    session.commit()
                    print(table_name)
                    print(low)
                    print(now_close)
                    print(low_price_1)
                    print(low_price_2)
                    print(low_price_3)
                    print('------------')
    Session.remove()


if __name__ == '__main__':
    taskBeat601069()
