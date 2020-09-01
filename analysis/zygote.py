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
from common.utils import Utils
from create_db import Session


# 算出最长 不涨 的日期长度，目前是否处于该位置
def task1(info, table_name):
    session = Session()
    resultProxy = session.execute('select pctChg from {}'.format(Utils.bornTableNameForNumber(table_name)))
    result = resultProxy.fetchall()
    max = 0
    now = 0
    for i, element in enumerate(result):
        if element[0] < 0:
            now += 1
        else:
            if now > max:
                max = now
            now = 0
    print('max   %d' % max)
    print('now   %d' % now)
    print('f3   %d' % info['f3'])


if __name__ == '__main__':
    task1()
