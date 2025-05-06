import re
import numpy as np
import requests

import mysql.connector

## Create/Connect to database
conn = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  password = '12345678',
  database = 'magazines'
)
## Create cursor, used to execute commands
cur = conn.cursor()
# cur.execute("""select * from magazines where download_links_nums > 0 and tags like "%海外剧集%";""")
cur.execute("""select * from magazines where download_links_nums = 0 and download_links like "%pan.baidu.com%";""")
datas = cur.fetchall() 

regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

for data in datas:
  # print(data)
  count = 0
  if data[4]:
    count += 1
  if data[9]:
    count += 1
  if data[10]:
    count += 1
  
  print(count)

  # cur.execute("""update magazines set download_links_nums = %s where id = %s;""", (count, data[0]))

  # if data[4] and len(data[4]) < 5:
  pure_download_links = str(list(filter(None, np.array(re.findall(regex, str(data[3]))).flatten())))
  print(pure_download_links)
  cur.execute("""update magazines set pure_download_links = %s where id = %s;""", (pure_download_links, data[0]))

conn.commit()