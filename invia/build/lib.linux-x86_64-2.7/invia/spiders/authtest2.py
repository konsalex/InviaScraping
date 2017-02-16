import scrapy

import re
from scrapy.selector import Selector
import json



class MySpider(scrapy.Spider):
    name = 'authtest2'
    start_urls = ['https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999']

    def start_requests(self):
        return [scrapy.FormRequest("https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999",
                                   formdata={'user': '', 'pass': ''},
                                   callback=self.after_login)]


    def after_login(self, response):
             
            return scrapy.Request(url="https://dovolena.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B%5D=28&nl_locality_id%5B%5D=19&d_start_from=08.06.2017&d_end_to=20.07.2017&nl_length_int%5B%5D=7%7C9&nl_length_int%5B%5D=10%7C12&nl_length_int%5B%5D=13%7C&nl_transportation_id%5B%5D=3&nl_ck_id%5B%5D=62&nl_ck_id%5B%5D=61&sort=nl_sell&page=1&getOptionsCount=true&base_url=https%3A%2F%2Fdovolena.invia.cz%2F",callback=self.logged_in)

    def logged_in(self, response):
        data=json.loads(response.text)
        selector=Selector(text=data['boxes_html'],type='html')

        
        yield{

          'data':selector.xpath('//li/@data-content-value').extract(),
          'touroperators':selector.css('a>div:nth-child(2)>p.r::text').extract()


             }

        print data['boxes_html']
        next_page = selector.css("a.next::attr(data-page)").extract_first()
        url = re.sub('page=\d+', 'page=' + next_page, response.url)
        yield scrapy.Request(url, self.logged_in)

