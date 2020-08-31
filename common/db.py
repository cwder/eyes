from create_db import Session
from common.utils import Utils


class Db:
    # 批量删除字端、段
    @staticmethod
    def deleteCol(self):
        session = Session()
        allTables = []
        tablesResultProxy = session.execute('show tables')
        tableKeys = tablesResultProxy.keys()
        for rowproxy in tablesResultProxy:
            for key in tableKeys:
                tName = Utils.formatTableName(rowproxy[key])
                delSql = 'alter table {} DROP COLUMN a1,DROP COLUMN a2,' \
                         'DROP COLUMN a3,DROP COLUMN a4,DROP COLUMN a5,DROP COLUMN a6,' \
                         'DROP COLUMN a7,DROP COLUMN a8,DROP COLUMN a9,DROP COLUMN a10,'.format(tName);
                session.execute(delSql)
        pass


if __name__ == '__main__':
    session = Session()
    tName = Utils.formatTableName('sh.600000')
    delSql = 'alter table {} DROP COLUMN a1,DROP COLUMN a2,' \
             'DROP COLUMN a3,DROP COLUMN a4,DROP COLUMN a5,DROP COLUMN a6,' \
             'DROP COLUMN a7,DROP COLUMN a8,DROP COLUMN a9,DROP COLUMN a10'.format(tName)
    session.execute(delSql)
