from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# 连接测试数据库
from sqlalchemy.orm import sessionmaker, scoped_session

from config.config import db_info
engine = create_engine(
    db_info["uri"],
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
# 基本类
Base = declarative_base()
