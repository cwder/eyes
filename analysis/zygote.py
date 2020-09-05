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
import math

from common.utils import Utils
from create_db import Session


# 算出最长 不涨 的日期长度，目前是否处于该位置
def task1(table_name, info=None):
    session = Session()
    resultProxy = session.execute(
        'select * from {} order by date asc'.format(Utils.bornTableNameForNumber(table_name)))
    result = resultProxy.fetchall()
    max = 0
    now = 0
    table_pctchg = 0
    for i, element in enumerate(result):
        table_pctchg = element['pctChg']
        if table_pctchg < 0:
            now += 1
        else:
            if now > max:
                max = now
            now = 0
    if now == 0:
        return


    if info is None:
        return
    info_res = info['f3']
    if info_res == '-' or info_res == '':
        return
    if info_res < 0 and math.isclose(info_res, Utils.floatTo2(table_pctchg) == False):
        now += 1
        if now > max:
            print('table----A ' + info['f14'] + ' ' + info['f12'])


if __name__ == '__main__':
    task1('600015')
