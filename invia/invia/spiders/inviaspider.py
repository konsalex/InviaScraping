import scrapy

#from scrapy.loader import ItemLoader
#from invia.items import inviaItems
import re
from scrapy.selector import Selector
import json



class InviaSpider(scrapy.Spider):
    name = 'Kreta'  
    start_urls = ['https://dovolena.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B0%5D=28&nl_locality_id%5B0%5D=19&d_start_from=08.06.2017&d_end_to=16.06.2017&nl_length_int%5B0%5D=7%7C9&nl_length_int%5B1%5D=10%7C12&nl_length_int%5B2%5D=13%7C&nl_transportation_id%5B0%5D=3&nl_ck_id%5B0%5D=62&nl_ck_id%5B1%5D=61&sort=nl_sell&page=1&getOptionsCount=true&base_url=https%3A%2F%2Fdovolena.invia.cz%2F']

    def parse(self, response):
       # download_delay=0.5
        data=json.loads(response.text)
        selector=Selector(text=data['boxes_html'],type='html')

        #names = response.css('span.name::text').extract()
        #for name in names:
         #   yield {'name': name}

        yield{

          'data':selector.xpath('//li/@data-content-value').extract()

             }

        # next page
        next_page = selector.css("a.next::attr(data-page)").extract_first()
        url = re.sub('page=\d+', 'page=' + next_page, response.url)
        yield scrapy.Request(url, self.parse)
        
        #if (response.css('#main > div > div > div > div.col.col-content > div.product-list > div > p > a.next').extract_first()):
         #  url = 'https://dovolena.invia.cz/?d_start_from=13.01.2017&sort=nl_sell&page={}'.format(y)
          # yield Request(url, self.parse, meta={'index':y})


