# f2:	最新价
# f3:	涨跌幅 %
# f4:	涨跌额
# f5:	成交量 手
# f6:	成交额
# f7:	震幅 %
# f8:	换手率 %
# f9:	市盈率 动态
# f10:	量比
# f11:	-
# f12:	股票编码
# f13:	-
# f14:	股票名
# f15:	最高价
# f16:	最低价
# f17:	今开
# f18:	昨收
# f20:	总市值
# f23:  市净率
# f115:	市盈率ttm

#   要用这里的每一行代码改变命运！！！！！

from create_db import Session

# 算出最长 不涨 的日期长度，目前是否处于该位置
def task1():
    session = Session()

    resultProxy = session.execute('select * from `000001`')
    resultProxy.c


if __name__ == '__main__':
    task1()
