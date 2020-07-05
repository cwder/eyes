# 面试人表
from sqlalchemy import Column, Integer, String

from create_db import Base, Session


class Shares(Base):
    __tablename__ = 'Shares'

    id = Column(Integer, autoincrement=True, primary_key=True)
    code = Column(String(10))
    name = Column(String(50))

    @staticmethod
    def addShares(code, name):
        try:
            info = Shares(code=code, name=name)
            session = Session()
            session.add(info)
            session.commit()
        except Exception as e:
            session.rollback()
