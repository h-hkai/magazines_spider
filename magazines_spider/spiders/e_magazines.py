from typing import Iterable
import numpy as np
import scrapy
import time
import re

from magazines_spider.items import MagazineItem

from .tools import Tools

class EMagazinesSpider(scrapy.Spider):
  name = "magazines"
  allowed_domains = ["e-magazines.top", "magsilo.com"]
  start_urls = ["https://e-magazines.top/", "https://magsilo.com/"]

  custom_settings = {
    'ITEM_PIPELINES': {
      "magazines_spider.pipelines.MagazinesSpiderPipeline": 300,
    }
  }

  def start_requests(self):
    for index in range(0, len(self.start_urls)):
      cookies = {data.split('=')[0]: data.split('=')[-1] for data in Tools.cookies_str[index].split('; ')}
      yield scrapy.Request(url=self.start_urls[index], cookies=cookies, callback=self.parse)

  def parse(self, response):
    for magazine in response.css('.home-tab-content .posts-row .posts-item'):
      url = magazine.css('.item-thumbnail a::attr(href)').extract_first()
      img = magazine.css('.item-thumbnail img::attr(data-src)').extract_first()
      update_time = magazine.css('.item-body .item-meta .meta-author').css('span::attr(title)').extract_first()
      yield scrapy.Request(url=url, callback=self.getItem, cb_kwargs=dict(img=img, update_time=update_time))
      # self.log("url = {}".format(url))
      # self.log("img = {}".format(img))
      # self.log("update_time = {}".format(update_time))
    next = response.css('.pagenav .next').css('a::attr(href)').extract_first()
    # self.log("next = {}".format(next))
    # time.sleep(16)
    if next is not None:
      yield scrapy.Request(url=next, callback=self.parse)

  def getItem(self, response, img, update_time):
    magazine_item = MagazineItem()
    title_zh = response.css('.article-header .article-title').css('a::text').extract_first()
    title_en = response.css('.article-content .wp-block-image .wp-element-caption ::text').extract_first()
    # self.log("title = {}".format(title_zh))

    download_links = response.css('.hidden-box .but-download').css('a::attr(href)').extract()
    # self.log("download_links = {}".format(download_links))

    # img = response.css('.article-content .wp-block-image').css('img::attr(src)').extract_first()

    description = response.css('.wp-block-zibllblock-quote .quote_q p::text').extract_first()
    # self.log("description = {}".format(description))

    tags = response.css('.article-content .article-tags').css('::text').extract()
    # self.log("tags = {}".format(tags))

    # update_time = response.css('.article-avatar .px12-sm').css('::text').extract_first()
    # self.log("update_time = {}".format(update_time))

    pure_download_links = None
    if "海外剧集" in tags:
      pure_download_links = response.css('.wp-block-zibllblock-hide-content p::text').extract()
      print("download_links = {}".format(pure_download_links))

    magazine_item['download_links'] = download_links
    magazine_item['pure_download_links'] = pure_download_links
    magazine_item['title_zh'] = title_zh
    magazine_item['title_en'] = title_en
    magazine_item['img'] = img 
    magazine_item['description'] = description
    magazine_item['tags'] = tags
    magazine_item['update_time'] = update_time

    yield magazine_item
