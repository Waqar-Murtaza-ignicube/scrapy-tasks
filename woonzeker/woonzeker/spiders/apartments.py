"Module to use scrapy and its classes"
import re
import scrapy
import chompjs
from woonzeker.items import WoonzekerItem

class RentSpider(scrapy.Spider):
    """spider class to scrape the web url"""
    name = "rentspider"
    allowed_domains = ["woonzeker.com"]
    start_urls = ["https://woonzeker.com/aanbod"]

    location_urls = {
        'p': 's-gravenhage',
        'ah': 'rotterdam',
        'ae': 'rijswijk',
        'aH': 'delft',
        'ai': 'voorburg',
        'dC': 'vlaardingen'
    }

    def parse(self, response):
        """parse method to scrape from response of website"""
        # Selecting the script tag containing the desired text
        data = response.xpath("//script[contains(text(), 'window.__NUXT')]/text()").get()

        # Extracting the content within the description:{content: ...} using regular expressions
        rent_list_match = re.search(r'rent:\[({.+?})\]', data)
        if rent_list_match:
            rent_list_content = rent_list_match.group()
            rental_list = chompjs.parse_js_object(rent_list_content)

            for item in rental_list:
                location = item['address'].get('location')
                if location in self.location_urls:
                    url = self.location_urls[location]
                else:
                    url = location
                slug = item["slug"]
                property_url = f"/{url}/{slug}"
                property_page = "https://woonzeker.com/aanbod" + property_url
                yield response.follow(property_page, callback=self.property_parser,
                                        cb_kwargs={"item": item})

    def extract_fields(self, response, field_key):
        """method to merge the same fields functionality"""
        field_value = response.xpath(f"//div[contains(text(), '{field_key}')]"
                                     "/following-sibling::div/text()")
        return field_value.get()

    def property_parser(self, response, item):

        """parsing the response from property url"""
        address = response.css(".header__text-location::text").get()
        postal_code, city = address.rsplit(' ', 1)

            # making a dic for items having similar selectors
        field_items = {
            'Prijs': 'price',
            'Woonoppervlakte:': 'surface',
            'kamers:': 'rooms',
            'slaapkamers:': 'bedrooms',
            'Oplevering': 'furniture'
        }

        extracted_items = {}
        for field_key, field_value in field_items.items():
            extracted_items[field_value] = self.extract_fields(response, field_key)

        house_item = WoonzekerItem()

        house_item["url"] = response.url
        house_item["address"]= item['title']
        house_item["city"]= city
        house_item["postal_code"]= postal_code
        house_item["latitude"]= item['address']['position_long']
        house_item["longitude"]= item['address']['position_long']
        house_item["price"]= extracted_items.get("price")
        house_item["rooms"]= extracted_items.get("rooms")
        house_item["bedrooms"]= extracted_items.get("bedrooms")
        house_item["surface"]= extracted_items.get("surface")
        house_item["furniture"]= extracted_items.get("furniture")
        house_item["photo"]= response.css(".header__images-first::attr(style)").get()
        house_item["description"]= response.css(".property-description__content::text").get()

        yield house_item
