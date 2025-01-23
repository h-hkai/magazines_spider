import scrapy
import requests

class LinkAiSpider(scrapy.Spider):
  name = "link-ai"
  allowed_domains = ["link-ai.tech"]
  start_urls = ["https://link-ai.tech"]

  def parse(self, response):
    datas = [{
      'username': '18737044521',
      'password': '18737044521'
    }, {
      'username': '17344381547',
      'password': '17344381547'
    }, {
      'username': '16533923763',
      'password': '16533923763'
    }, {
      'username': '16524786409',
      'password': '16524786409'
    }]
    for data in datas:
      self.dailySignin(data)

  def dailySignin(self, data):
    s = requests.Session()  # 初始化Session对象
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

    response1 = s.post(url='https://link-ai.tech/api/login', data=data, headers=headers)
    json_response1 = response1.json()
    token = json_response1['data']['token']

    headers['authorization'] = f'Bearer {token}'

    # daily signin
    response2 = s.get(url='https://link-ai.tech/api/chat/web/app/user/sign/in', headers=headers)
    print(response2.text)
