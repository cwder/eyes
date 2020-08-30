import baostock as bs
import pandas as pd

from common.utils import Utils

lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

rs = bs.query_history_k_data_plus("sh.600234",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
    start_date='2020-08-01',
    frequency="d", adjustflag="3") #frequency="d"取日k线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
# end_date='2020-08-11',
#
# #### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    # data_list.append(rs.get_row_data())
    print(rs.get_row_data())
# result = pd.DataFrame(data_list, columns=rs.fields)
# #### 结果集输出到csv文件 ####
# result.to_csv("D:/history_k_data.csv", encoding="gbk", index=False)
# print(result)
# print(Utils.getTime())
# rs = bs.query_all_stock(day="2020-08-28")
# while (rs.error_code == '0') & rs.next():
#     tableName = rs.get_row_data()[0]
#     print(tableName)
#### 登出系统 ####
bs.logout()