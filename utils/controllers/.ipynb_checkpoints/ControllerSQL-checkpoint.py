
from logging import getLogger
import traceback
from os import getenv
from pandas import read_sql_query
from sqlalchemy.engine.url import URL
from sqlalchemy import text
from sqlalchemy import create_engine
from datetime import datetime,timedelta
from pandas import DataFrame
from pandas import concat
from json import loads as loads_

message = 'SQLController'


class ControllerSQL:
    def __init__(self):

        self.error = False
        self.url_string= None
        self.metadata = None
        self.session = None
        self.engine = None
        self.region_name = None
        
        self.driver = 'mysql+mysqldb'
        self.MYSQL_DATABASE = getenv("MYSQL_DATABASE")
        self.MYSQL_USER = getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
        self.MYSQL_HOST = getenv("MYSQL_HOST")
        self.MYSQL_PORT = getenv("MYSQL_PORT")
        self.prefix = getenv("ENV") + '_'
        self.date_format= '%Y-%m-%dT%H:%M:%S'

        # set self.url_string
        self.get_url()

        self.logger = getLogger(message)

        # Init ()
        self.logger.info("donde init method of Controller")
          
    def get_url(self):
        
        # dialect+driver://username:password@host:port/database
        # build the sqlalchemy URL
        self.url_string = URL.create(
            drivername=self.driver,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            database=self.MYSQL_DATABASE,
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD
            )

    def get_conection(self) -> None:

        self.logger.info("call get_conection() method of Controller ")
        try:
                
                self.engine = create_engine(self.url_string)

                
        except Exception as e:
            print(e)
            self.logger.error('error  get_conection')

        self.logger.info(" Done get_conection() method of Controller")

    def close_conection(self):          
        self.session.close() 
        self.engine.dispose()

    def execute_query(self,query=None):
        return read_sql_query(text(query),self.engine)   
