import scrapy
from re import findall, sub
from ..itemsloader import ListingItemLoaders
from ..items import ListItem


class NpcdotcomSpider(scrapy.Spider):
    name = "npcdotcom"
    allowed_domains = ["nigeriapropertycentre.com"]
    start_urls = ["https://nigeriapropertycentre.com/all-property?added=30&page=1"]
    
    '''This method gets each of the 21 links in each page and then follows the link to the next page.
    The page where Scrapy last stopped is recorded and called back to the next method.'''
    def parse(self, response):
        # Get the page number from link string
        page_num = int(page_num_str) # converted to number
        # Loop over each listing link in the page
        for listing in response.xpath('//a[@itemprop="url"]/@href').getall():
            # Callback this link in the next method
            yield scrapy.Request(
                url='https://'+self.allowed_domains[0]+listing, callback=self.listing_parse, meta={'page number':str(page_num)})
        # Form next page from url
        next_page = sub(r'[0-9]+$',str(page_num+1), response.url)
        if page_num>10:
            return
        # Callback next page to same method and start scraping process again
        yield scrapy.Request(
            url=next_page, callback=self.parse)

    '''This method opens each listing and gets particular items from it.
    Then items are loaded and sent to itemloaders'''
    def listing_parse(self, response):
        listitems = ListingItemLoaders(ListItem(), response) #create an instance of the listitemloaders class
        # add items by name and value/xpath
        listitems.add_xpath('ref', '//strong[text()="Property Ref:"]/following-sibling::text()')
        listitems.add_value('url', response.url)
        listitems.add_value('page', response.meta.get('page number')) #1.
        listitems.add_xpath('price_ngn', '//span[@itemprop="price"]/text()')
        listitems.add_xpath('period', '//span[@class="period"]/text()')
        listitems.add_xpath('bedroom', '//strong[text()="Bedrooms:"]/following-sibling::text()')
        listitems.add_xpath('bathroom', '//strong[text()="Bathrooms:"]/following-sibling::text()')
        listitems.add_xpath('toilet', '//strong[text()="Toilets:"]/following-sibling::text()')
        listitems.add_xpath('parking', '//strong[text()="Parking Spaces:"]/following-sibling::text()')
        listitems.add_xpath('area_sqm', '//strong[text()="Total Area:"]/following-sibling::text()') #2.
        listitems.add_xpath('listdate', '//strong[text()="Last Updated:"]/following-sibling::text()')
        listitems.add_xpath('listtype', '//strong[text()="Type:"]/following-sibling::text()')
        listitems.add_xpath('details', '//p[@itemprop="detailsription"]/text()')
        listitems.add_xpath('address', '//address/text()') #3.
        listitems.add_xpath('marketer', '//div[@class="panel-body"]//strong/text()')
        listitems.add_xpath('contact', '//i[@class="fab fa-whatsapp fa-fw"]/following-sibling::text()') #4.
        yield listitems.load_item() # yield to scrapy