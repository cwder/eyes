import datetime
import time


class Utils:
    @staticmethod
    def getTime():
        return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def getTableName(name):
        s1 = '`'
        tName = "{}{}{}".format(s1, name, s1)
        return tName

    @staticmethod
    def getTableString(field):
        s1 = '\''
        field = "{}{}{}".format(s1, field, s1)
        return field

    @staticmethod
    def makeArrNotNull(array, default):
        for i in range(0, len(array)):
            if array[i] is None or array[i] == '':
                array[i] = default
        return array

    @staticmethod
    def compareDate(date1, date2, fmt='%Y-%m-%d'):
        """
            比较两个真实日期之间的大小，date1 > date2 则返回True
            :param date1:
            :param date2:
            :param fmt:
            :return:
            """

        zero = datetime.datetime.fromtimestamp(0)
        try:
            d1 = datetime.datetime.strptime(str(date1), fmt)
        except:
            d1 = zero
        try:
            d2 = datetime.datetime.strptime(str(date2), fmt)
        except:
            d2 = zero
        return d1 > d2


if __name__ == '__main__':
    a = '2020-09-01'
    d1 = datetime.datetime.strptime(a, '%Y-%m-%d')
    print(a)
