# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SgmarineProfilesItem(scrapy.Item):
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_address = scrapy.Field()
    company_phone_number = scrapy.Field()
    company_email = scrapy.Field()
    company_website = scrapy.Field()
    company_description = scrapy.Field()
    company_product_services = scrapy.Field()   # {url, img, title}
    company_categories = scrapy.Field()
