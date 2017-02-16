import scrapy
import re
from scrapy.selector import Selector
import json


class LoginSpider(scrapy.Spider):
    name = 'auth'
    start_urls = ['https://www.invia.cz/']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'zisi@electratours.cz', 'password': 'electra1999'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            print "sou gamaw thn mana"
            self.logger.error("Login failed")
            return
        else:
            print "nai re gamw thn mana sou"
            DOWNLOAD_DELAY = 5 
            return scrapy.Request(url="https://dovolena.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B0%5D=28&nl_locality_id%5B0%5D=19&d_start_from=08.06.2017&d_end_to=16.06.2017&nl_length_int%5B0%5D=7%7C9&nl_length_int%5B1%5D=10%7C12&nl_length_int%5B2%5D=13%7C&nl_transportation_id%5B0%5D=3&nl_ck_id%5B0%5D=62&nl_ck_id%5B1%5D=61&sort=nl_sell&page=1&getOptionsCount=true&base_url=https%3A%2F%2Fdovolena.invia.cz%2F",callback=self.parse_starting)


    def parse_starting(self,response):
        data=json.loads(response.text)
        selector=Selector(text=data['boxes_html'],type='html')

        
        yield{

           'testaki':data['boxes_html']

          #'data':selector.xpath('//li/@data-content-value').extract()

             }

        # next page
        #next_page = selector.css("a.next::attr(data-page)").extract_first()
        #url = re.sub('page=\d+', 'page=' + next_page, response.url)
        #yield scrapy.Request(url, self.parse_starting)
        