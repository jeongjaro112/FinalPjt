# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    종목명 = scrapy.Field()
    종목코드 = scrapy.Field()
    시장구분 = scrapy.Field()
    업종구분 = scrapy.Field()
    상세구분 = scrapy.Field()
    투자의견 = scrapy.Field()
    현재가 = scrapy.Field()
    매출액 = scrapy.Field()
    순이익 = scrapy.Field()
    순이익율 = scrapy.Field()
    PER = scrapy.Field()
    PBR = scrapy.Field()
    ROE = scrapy.Field()
    EV_EBITDA = scrapy.Field()
    배당수익율 = scrapy.Field()
    부채비율 = scrapy.Field()
    
