import scrapy
import re
from scrapy.selector import Selector
import json



class MySpider(scrapy.Spider):
    name = 'naming'
    

    start_urls = ['https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999']

    

    def start_requests(self):
        return [scrapy.FormRequest("https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999",
                                   formdata={'user': '', 'pass': ''},
                                   callback=self.after_login)]


    def after_login(self, response):
             
            return scrapy.Request(url="https://dovolena.invia.cz/direct/tour_search/ajax-next-boxes/?d_start_from=09.02.2017&nl_ck_id%5B%5D=62&sort=nl_sell&page=1&getOptionsCount=true&base_url=https%3A%2F%2Fdovolena.invia.cz%2F",callback=self.logged_in)

    def logged_in(self, response):
        

        data=json.loads(response.text)

        sel=Selector(text=data['boxes_html'])
       
        names=sel.css('span.name::text').extract()
       
        InviaCode=sel.css('div.wrap>div>p:nth-child(4)::text').re(r'(?<=: )[^\]]+')

        Op=sel.css('a>div:nth-child(2)>p.r::text').extract_first()

        print (Op)
       
       # dest=sel.css('p.location').re(r'cko ([^<]*)<')     #.re(r'>([^<]*)<')
        
        
        
        for x in range(0,len(names)):
          yield{
               #if InviaCode[x] is None: 'InviaCode':null,
               #else: 'InviaCode': InviaCode[x],
               #'InviaCode'InviaCode[x],
               'HotelName':names[x]
               #'Destination':dest
                 }

         #     'InviaCode':InviaCode[x],
           #    'HotelName':names[x],
             #'Destination':dest[x]           
                

        next_page = sel.css("a.next::attr(data-page)").extract_first()
        print("Page %s -1" %next_page)
        url = re.sub('page=\d+', 'page=' + next_page, response.url)
        yield scrapy.Request(url, self.logged_in)

   