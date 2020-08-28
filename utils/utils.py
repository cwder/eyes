from datetime import date, datetime
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


if __name__ == '__main__':
    a = Utils.getTableString('2020-09-01')
    print(a)
