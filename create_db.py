from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

#  todo 确认连接生产数据库
# engine = create_engine(
#     'mysql+pymysql://wonderexam:HUIHDHDOIDJNPPJ@116.206.198.17:3306/wonderexam?charset=utf8',
#     echo=True)

# 连接测试数据库
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(
    'mysql+pymysql://root:111111@localhost:3306/eyes?charset=utf8mb4',
    echo=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
# 基本类
Base = declarative_base()
from model.models import *

# def a():
#     t = type("hello", (Base,), {"__tablename__": "hello", "id": Column(Integer, autoincrement=True, primary_key=True)})

t = type("hello", (Base,), {"__tablename__": "hello", "__table_args__": {'extend_existing': True},
                            id: Column(Integer, autoincrement=True, primary_key=True)})

# a()
# 创建表
Base.metadata.create_all(engine)
