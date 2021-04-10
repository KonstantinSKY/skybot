################################################################################
# Script name : sql_init.py                      Date   : 04/10/2021           #
# Author      : Stan SKY                         E-mail : sky012877@gmail.com  #
# Description : init db                                                        #
################################################################################
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine =  create_engine('sqlite:///DB/test.db', echo=True)
Base = declarative_base()


