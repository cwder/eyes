from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, String

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

# 创建表
Base.metadata.create_all(engine)
