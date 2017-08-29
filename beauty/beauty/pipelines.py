# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding("utf8")

import urllib
import pymysql
import os, os.path
from beauty.settings import IMAGES_STORE, MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USR, MYSQL_PWD, MYSQL_CHARSET

class BeautyPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host = MYSQL_HOST,
            port = MYSQL_PORT,
            user = MYSQL_USR,
            passwd = MYSQL_PWD,
            db = MYSQL_DB,
            charset = MYSQL_CHARSET,
        )

        self.insert_sql = "insert into meizi(category, title, url, update_time, click_amount, tags, content) values('%s', '%s', '%s', '%s', '%s', '%s', '%s');"

    def process_item(self, item, spider):

        # 数据存储
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(self.insert_sql % (item['category'], item['title'],  item['url'], item['update_time'], item['click_amount'], item['tags'], item['content']))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

        # 图片下载
        category = item['category'].replace(u"/", u"-").replace(u"?", u"").replace(u"\\", u"-")
        title = item['title'].replace(u"/", u"-").replace(u"?", u"").replace(u"\\", u"-")
        url = item['url']
        file_name = url.split(u"/")[-1].replace(u"/", u"-").replace(u"?", u"").replace(u"\\", u"-")
        file_path = os.path.join(IMAGES_STORE, category, title)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_path = os.path.join(file_path, file_name)
        if not os.path.exists(file_path):
            urllib.urlretrieve(url, file_path)

        return item
