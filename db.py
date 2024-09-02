from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
from sqlalchemy.orm import declarative_base
import pymysql

pymysql.install_as_MySQLdb()

engine = create_engine("mysql+pymysql://root:vttp1003@localhost:3306/vnexpress")

connection = engine.connect()

Base = declarative_base()

class news(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    link = Column(TEXT)
    description = Column(LONGTEXT)
    image = Column(TEXT)
    title = Column(TEXT)


Base.metadata.create_all(engine)