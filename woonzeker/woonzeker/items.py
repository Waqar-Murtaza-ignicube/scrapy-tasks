"Module to use scrapy and its classes"
import scrapy

class WoonzekerItem(scrapy.Item):
    """class to use scrapy item fields"""
    url = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    postal_code = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    bedrooms = scrapy.Field()
    surface = scrapy.Field()
    furniture = scrapy.Field()
    photo = scrapy.Field()
    description = scrapy.Field()
