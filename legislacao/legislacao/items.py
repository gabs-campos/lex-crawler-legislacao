# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LegislacaoItem(scrapy.Item):
    esfera = scrapy.Field()
    numero = scrapy.Field()
    ano = scrapy.Field()
    ementa = scrapy.Field()
    integra = scrapy.Field()
    url = scrapy.Field()
    embedding = scrapy.Field()