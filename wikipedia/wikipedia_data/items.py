# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

class PageData(scrapy.Item):
    pagedata = scrapy.Field()
    date = scrapy.Field()
    # title = scrapy.Field(output_processor=TakeFirst())
    # href = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(utils.geizhals_visit_url))
    # price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(utils.geizhals_price2float))
    # set_id = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(utils.get_lego_id_from_title))
    # merchant = scrapy.Field(output_processor=TakeFirst())
    # #availibility = scrapy.Field(output_processor=TakeFirst(
