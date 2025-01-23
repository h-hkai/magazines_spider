import scrapy
import requests
from pyquery import PyQuery as pq

class Pojie52Spider(scrapy.Spider):
  name = "52pojie"
  allowed_domains = ["www.52pojie.cn"]
  start_urls = ["https://www.52pojie.cn"]

  cookie="htVC_2132_saltkey=JK64KImq; htVC_2132_auth=82eck9VvV89oxyeJk9NFu34cTXg2pIOqV3HVK%2BjonNnPTQqQyFF1U%2Fjsun9DfyCpZsTtOFpUhWjZ%2Bpxl2FuvF2MctPWk"
  if not cookie:
      cookie = input("cookie")
  sckey = 'SCT256309T8D6Sn2WpIVzGDELwhYaUQo2h'
  url = 'https://www.52pojie.cn/home.php?mod=task&do=draw&id=2'
  url1 = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
  headers = {'cookie':cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4265.0 Safari/537.36 Edg/87.0.644.4'}
  requests.get(url1, headers=headers)
  req = requests.get(url, headers=headers).text
      
  doc = pq(req)
  msg = doc('.vwmy a').text() + '\t' + doc('#messagetext p').text()
  print(msg)
  if not cookie:
    print('cookie为空')
  if sckey:
    send_url = f'https://sctapi.ftqq.com/{sckey}.send?title={msg}'
    requests.get(send_url)
