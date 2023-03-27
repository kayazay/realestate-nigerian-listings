import scrapy.loader
from itemloaders.processors import *


class ListingItemLoaders(scrapy.loader.ItemLoader):
    default_input_processor = MapCompose(lambda x: x.replace(r'\xa0','').replace(r'\n', '').strip())
    default_output_processor = TakeFirst()
    '''specific functions for specific items.
    '''
    price_ngn_out = Compose(
        TakeFirst(),
        lambda x: x.replace(',', '')
    ) # remove commas from price_ngn
    area_sqm_out = Compose(
        TakeFirst(),
        lambda x: x.replace(' sqm', '').replace(',', '')
    ) # remove unit of measurement and thousand delimeter
    def contactdoer(ceeitem):
        ceeitem = ceeitem.replace('+', '')
        first_3 = ceeitem[:3]
        return '0'+ceeitem[3:] if first_3=='234' else ceeitem
    contact_out = Compose(
        TakeFirst(),
        contactdoer,
    ) # number must start with 0 and no country code
    details_out = Join()
