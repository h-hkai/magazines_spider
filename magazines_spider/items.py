# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class MagazineItem(scrapy.Item):
  title_zh = Field()
  title_en = Field()
  download_links = Field()
  pure_download_links = Field()
  img = Field()
  description = Field()
  tags = Field()
  update_time = Field()
  table_name = Field()

class ItCourseItem(scrapy.Item):
  title = Field()
  dummy_download_links = Field()
  download_names = Field()
  download_links = Field()
  downcodes = Field()
  img = Field()
  description = Field()
  tags = Field()
  update_time = Field()
