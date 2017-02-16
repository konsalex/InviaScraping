# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class InviaItems(scrapy.Item):
   InviaCode = scrapy.Field()
   Dates=scrapy.Field()
   MealType=scrapy.Field()
   PeriodStart=scrapy.Field()
   PeriodEnd=scrapy.Field()
   Operator=scrapy.Field()
   Price=scrapy.Field()
