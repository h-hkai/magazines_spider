# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import time
import mysql.connector

class MagazinesSpiderPipeline:
  def __init__(self):
    ## Create/Connect to database
    self.conn = mysql.connector.connect(
      host = 'localhost',
      user = 'root',
      password = '12345678',
      database = 'magazines'
    )
    ## Create cursor, used to execute commands
    self.cur = self.conn.cursor()

    ## Create e-magezines table if none exists
    self.cur.execute("""
    CREATE TABLE IF NOT EXISTS magazines(
      id int NOT NULL auto_increment,
      title_zh text,
      title_en text,
      download_links text,
      img text,
      description text,
      tags text,
      update_time timestamp,
      PRIMARY KEY (id)
    )                 
    """)

  def process_item(self, item, spider):
    ## Check to see if text is already in database
    self.cur.execute("""select id from magazines where title_zh = %s""", (str(item['title_zh']),))
    result = self.cur.fetchone()

    # print("result.id = {}".format(result[0]))

    ## if it is in DB, update data
    if result:
      self.cur.execute("""update magazines set download_links = %s, update_time = %s where id = %s""", (
        str(item['download_links']),
        item['update_time'],
        result[0]
      ))
    else:
      ## Define insert statament
      if item['pure_download_links'] is not None:
        self.cur.execute("""insert into magazines (title_zh, title_en, download_links, pure_download_links, img, description, tags, update_time) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (
          item['title_zh'],
          item['title_en'],
          str(item['download_links']),
          str(item['pure_download_links']),
          item['img'],
          item['description'],
          str(item['tags']),
          item['update_time']
        ))
      else:
        self.cur.execute("""insert into magazines (title_zh, title_en, download_links, img, description, tags, update_time) values (%s, %s, %s, %s, %s, %s, %s)""", (
          item['title_zh'],
          item['title_en'],
          str(item['download_links']),
          item['img'],
          item['description'],
          str(item['tags']),
          item['update_time']
        ))

    ## Execte insert of data into database
    self.conn.commit()
    return item

  def close_spider(self, spider):
    ## Close cursor & connection to database
    self.cur.close()
    self.conn.close()


class CoursesSpiderPipeline:
  def __init__(self):
    ## Create/Connect to database
    self.conn = mysql.connector.connect(
      host = 'localhost',
      user = 'root',
      password = '12345678',
      database = 'courses'
    )
    ## Create cursor, used to execute commands
    self.cur = self.conn.cursor()

    ## Create e-magezines table if none exists
    self.cur.execute("""
    CREATE TABLE IF NOT EXISTS courses(
      id int NOT NULL auto_increment,
      title text,
      dummy_download_links text,
      download_names text,
      download_links text,
      downcodes text,
      img text,
      description text,
      tags text,
      update_time timestamp,
      PRIMARY KEY (id)
    )                 
    """)

  def process_item(self, item, spider):

    self.cur.execute("""insert into courses (title, dummy_download_links, download_names, download_links,\
     downcodes, img, description, tags, update_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
      item['title'],
      str(item['dummy_download_links']),
      str(item['download_names']),
      str(item['download_links']),
      str(item['downcodes']),
      item['img'],
      str(item['description']),
      str(item['tags']),
      item['update_time']
    ))

    ## Execte insert of data into database
    self.conn.commit()
    return item

  def close_spider(self, spider):
    ## Close cursor & connection to database
    self.cur.close()
    self.conn.close()