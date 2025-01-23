import scrapy
import numpy as np
import re

import mysql.connector

from magazines_spider.items import ItCourseItem
from .tools import Tools

class ItcoursesSpider(scrapy.Spider):
  name = "itcourses"
  allowed_domains = ["www.itxbzxw.com"]
  start_urls = ["https://www.itxbzxw.com/all"]

  custom_settings = {
    'ITEM_PIPELINES': {
      "magazines_spider.pipelines.CoursesSpiderPipeline": 300,
    }
  }

  handle_httpstatus_list = [301, 302]
  cookies = {data.split('=')[0]: data.split('=')[-1] for data in Tools.itcourses_cookies_str[0].split('; ')}

  ## Create/Connect to database
  conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '12345678',
    database = 'magazines'
  )
  ## Create cursor, used to execute commands
  cur = conn.cursor()

  def existed(self, title):
    self.cur.execute("""select * from itcourses where title = %s;""", (title,))
    courses = self.cur.fetchone() 
    if courses:
      return True
    return False


  def start_requests(self):
    # self.log("cookies = {}".format(cookies))
    yield scrapy.Request(url=self.start_urls[0], cookies=self.cookies, callback=self.parse)


  def parse(self, response):
    for course in response.css('.posts .post'):
      # self.log("course = {}".format(course))
      url = course.css('.img a::attr(href)').extract_first()
      img = course.css('.img img::attr(data-src)').extract_first()
      update_time = course.css('.grid-meta').css('span::text').extract_first()
      yield scrapy.Request(url=url, callback=self.getItem, cb_kwargs=dict(img=img, update_time=update_time))
      # self.log("url = {}".format(url))
      # self.log("img = {}".format(img))
      # self.log("update_time = {}".format(update_time))
    next = response.css('.pagination .next-page').css('a::attr(href)').extract_first() 
    if next is not None:
      yield scrapy.Request(url=next, callback=self.parse)
    pass

  def getItem(self, response, img, update_time):
    itcourses_item = ItCourseItem()
    title = response.css('.article-header').css('h1::text').extract_first()
    # self.log("title = {}".format(title))
    dummy_download_links = response.css('.article-content .erphpdown-box').css('a::attr(href)').extract_first()
    # self.log("dummy_download_links = {}".format(dummy_download_links))
    description = response.css('.article-content').css('p::text').extract()
    # self.log("description = {}".format(description))
    tags = response.css('.breadcrumbs').css('span::text').extract()
    if '首页' in tags: 
      tags.remove('首页')
    if '学习中心' in tags: 
      tags.remove('学习中心')
    if '正文' in tags: 
      tags.remove('正文')
    # self.log("tags = {}".format(tags))

    itcourses_item['title'] = title
    itcourses_item['dummy_download_links'] = dummy_download_links
    itcourses_item['download_names'] = []
    itcourses_item['download_links'] = []
    itcourses_item['downcodes'] = []
    itcourses_item['img'] = img
    itcourses_item['update_time'] = update_time
    itcourses_item['description'] = description
    itcourses_item['tags'] = tags

    # TypeError: Request url must be str, got NoneType
    if not self.existed(title) and dummy_download_links:
      yield scrapy.Request(url=dummy_download_links, cookies=self.cookies, 
                           callback=self.parseDummyDownloadLinks, cb_kwargs=dict(item=itcourses_item))

  def parseDummyDownloadLinks(self, response, item):
    download_links = response.css('.content').css('.erphpdown-msg').css('p')
    prefix_url = "https://www.itxbzxw.com/wp-content/plugins/erphpdown/"
    # for download_link in download_links:
    short_url = download_links[0].css("a::attr(href)").extract_first()
    # print("url = {}".format(url))
    url = prefix_url + short_url
    download_name = download_links[0].css("span::text").extract_first()
    # print("download_name = {}".format(download_name))
    downcode = download_links[0].css(".erphpdown-code").css("::text").extract_first()
    # print("downcode = {}".format(downcode))
    item['download_names'].append(download_name)
    item['downcodes'].append(downcode)
    # print("item = {}".format(item))
    yield scrapy.Request(url=url, cookies=self.cookies, 
                        callback=self.parseDownloadLinks, cb_kwargs=dict(item=item))

    # if item['download_links']:
    #   print("item['download_links'] = {}".format(item['download_links']))
    #   yield item

  def parseDownloadLinks(self, response, item):
    # print(response.status)
    # print(response.headers)
    if response.status == 302:
      # print(list(filter(None, np.array(re.findall(self.regex, str(response.headers['Location']))).flatten())))
      # download_link = str(list(filter(None, np.array(re.findall(Tools.regex, str(response.headers['Location']))).flatten())))
      download_link = str(response.headers['Location'])[2:-1]

      prefix = "https://www.itxbzxw.com/wp-content/plugins/erphpdown/"
      url = prefix + download_link

      yield scrapy.Request(url=url, cookies=self.cookies, 
                          callback=self.getDownloadLinks, cb_kwargs=dict(item=item))

  def getDownloadLinks(self, response, item):
    # print(response.status)
    # print(response.headers)
    # print(response.text)
    download_link = str(list(filter(None, np.array(re.findall(Tools.regex, str(response.text))).flatten())))
    item['download_links'].append(download_link)
    yield item