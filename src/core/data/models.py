from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Apis(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))  # GET, POST, PUT, DELETE等
    method = Column(String(10))  # GET, POST, PUT, DELETE等
    url = Column(String(100))  # 修改为100字符限制
    params = Column(Text, default="{}")  # 参数字段
    data = Column(Text, default="{}")  # 数据字段
    json = Column(Text, default="{}")  # JSON字段
    files = Column(Text, default="{}")  # 文件上传字段
    res_body = Column(Text, default="{}")  # 接口返回格式
    created_time = Column(DateTime, server_default=func.now())  # 创建时间
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())  # 更新时间


class Account_Cookies(Base):
    __tablename__ = "account_cookies"

    id = Column(Integer, primary_key=True, index=True)
    env = Column(String(50))  # 环境
    username = Column(String(50))  # 用户名
    cookie = Column(String(1000), nullable=True)  # 数据字段，允许为空
    created_time = Column(DateTime, server_default=func.now())  # 创建时间
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())  # 更新时间
