import scrapy
import re
import numpy as np
import requests

import mysql.connector

from scrapy.selector import Selector

from .tools import Tools

class CleandownloadlinksSpider(scrapy.Spider):
  name = "cleanDownloadLinks"
  allowed_domains = ["e-magazines.top", "magsilo.com"]

  ## Create/Connect to database
  conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '12345678',
    database = 'magazines'
  )
  ## Create cursor, used to execute commands
  cur = conn.cursor()
  cur.execute("""select * from magazines where download_links_nums = 0 and (img like '%magsilo%') order by update_time desc limit 400;""")
  z_datas = cur.fetchall() 
  cur.execute("""select * from magazines where download_links_nums = 0 and (img like '%magazines%') order by update_time desc limit 400;""")
  e_datas = cur.fetchall() 
  datas = [e_datas] + [z_datas]

  handle_httpstatus_list = [301, 302]

  def start_requests(self):
    # print(len(self.datas))
    for index in range(len(self.datas)):
      for data in self.datas[index]:
        download_links = str(data[3]) 
        magazine_id = data[0]
        dummy_links = list(filter(None, np.array(re.findall(Tools.regex, download_links)).flatten()))
        # print(dummy_links)
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in Tools.cookies_str[index].split('; ')}
        if len(dummy_links) > 0:
          # dummy_links[0] = "https://magsilo.com/pay-download/1635?key=aac5fec25e&down_id=0"
          for i in range(len(dummy_links)):
            yield scrapy.Request(url=dummy_links[i], cookies=cookies, 
                                 callback=self.parse, cb_kwargs=dict(id=magazine_id))

  def parse(self, response, id):
    # print(response.status)
    # print(response.headers)
    if response.status == 302:
      # print(list(filter(None, np.array(re.findall(self.regex, str(response.headers['Location']))).flatten())))
      pure_download_links = str(list(filter(None, np.array(re.findall(Tools.regex, str(response.headers['Location']))).flatten())))

      count = 0
      if pure_download_links.find("baidu") > 0:
        count += 1
        self.cur.execute("""update magazines set pure_download_links = %s where id = %s;""", (pure_download_links, id))
      elif pure_download_links.find("lanzoup") > 0:
        count += 1
        self.cur.execute("""update magazines set lanzoup_download_links = %s where id = %s;""", (pure_download_links, id))
      elif pure_download_links.find("kdocs") > 0:
        count += 1
        self.cur.execute("""update magazines set kdocs_download_links = %s where id = %s;""", (pure_download_links, id))

      self.cur.execute("""update magazines set download_links_nums = %s where id = %s;""", (count, id))
 
      self.conn.commit()
    pass
