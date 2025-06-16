# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class V1Item(scrapy.Item):
    # title = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    fuel = scrapy.Field()
    mileage = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()
    mec = scrapy.Field()
    couleur = scrapy.Field()
