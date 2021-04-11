################################################################################
# Script name : sql_init.py                      Date   : 04/10/2021           #
# Author      : Stan SKY                         E-mail : sky012877@gmail.com  #
# Description : init db                                                        #
################################################################################
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime, String

engine =  create_engine('sqlite:///DB/test.db', echo=True)
Base = declarative_base()

class Quotes(Base):
    __tablename__ = 'Quotes'
    id = Column(Integer, primary_key=True)
    instrument = Column(String, nullable=False )
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False) 
    volume = Column (Integer, nullable=False)
    time = Column(DateTime, nullable=False)

Base.metadata.create_all(engine)
print(Quotes)
