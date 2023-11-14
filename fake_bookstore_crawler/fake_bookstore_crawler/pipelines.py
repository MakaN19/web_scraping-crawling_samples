import os
import logging

import MySQLdb

from scrapy.spiders import CrawlSpider


logging.getLogger('__main__')
logging.basicConfig(level=logging.INFO)

# 127.0.0.1 for local testing - can't be localhost, must have force TCP/IP
# connection to prevent socket errors
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWD = os.getenv("DB_PASSWD")
DB = os.getenv("DB_NAME")


class MySQLDB:
    def __init__(self, host: str, user: str, passwd: str, db: str) -> None:
        self.conn_ = self.create_connection(host, user, passwd, db)
        self.cursor_ = self.conn_.cursor()

    def create_connection(self, host: str, user: str, passwd: str, db: str) -> None:
        return MySQLdb.connect(
            host=host,
            user=user,
            passwd=passwd,
            db=db,
            port=3306,
            unix_socket="")

    def close_conection(self):
        self.conn_.close()

    def execute_query(self, query: str) -> None:
        self.cursor_.execute(query)
        self.conn_.commit()

    def __del__(self):
        try:
            self.close_conection()
        except:
            pass


class FakeBookstoreCrawlerPipeline:
    def __init__(self):
        self.db_ = None

    def open_spider(self, spider: CrawlSpider) -> None:
        logging.info("Spider opened from pipeline: %s" % spider.name)
        self.db_ = MySQLDB(HOST, USER, PASSWD, DB)
        self.db_.execute_query("""CREATE TABLE IF NOT EXISTS items (
                                    title varchar(255),
                                    price varchar(255)
                                 );""")

    def close_spider(self, spider: CrawlSpider) -> None:
        logging.info("Spider closed from pipeline: %s" % spider.name)
        self.db_.close_conection()

    def process_item(self, item: dict, spider: CrawlSpider) -> None:
        logging.info(item)
        self.db_.execute_query(
            """INSERT INTO items (title, price)
               VALUES ("{title}", "{price}");""".format(title=item["title"], price=item["price"]))
