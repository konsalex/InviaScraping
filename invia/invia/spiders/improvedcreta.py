import scrapy
import re
from scrapy.selector import Selector
import json



class MySpider(scrapy.Spider):
    name = 'Kretaimp'
    start_urls = ['https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999']
    

    def start_requests(self):
        return [scrapy.FormRequest("https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999",
                                   formdata={'user': '', 'pass': ''},
                                   callback=self.after_login)]


    def after_login(self, response):
             
            return scrapy.Request(url="https://dovolena.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B%5D=28&nl_locality_id%5B%5D=19&d_start_from=09.06.2017&d_end_to=16.06.2017&nl_length_int%5B%5D=7%7C9&nl_length_int%5B%5D=10%7C12&nl_length_int%5B%5D=13%7C&nl_transportation_id%5B%5D=3&sort=nl_sell&page=1&getOptionsCount=true&base_url=https%3A%2F%2Fdovolena.invia.cz%2F",callback=self.logged_in)

    def logged_in(self, response):
        data=json.loads(response.text)

        sel=Selector(text=data['boxes_html'])
        ag=Selector(text=data['boxes_html'])
        ko=sel.css('li.hotel-box').extract()  

        for x in range(0,len(ko)):
          sel=Selector(text=ko[x])

          name=sel.css('span.name::text').extract_first()

          data=sel.xpath('//li/@data-content-value').extract()

          Op=sel.css('a>div:nth-child(2)>p.r::text').extract()

          IC=[json.loads(d)["nl_hotel_id"] for d in data]
        
          PS=[json.loads(d)["d_start"] for d in data]

          PD=[json.loads(d)["d_end"] for d in data]

          PR=[json.loads(d)["c_price_from"] for d in data]

          Dates=sel.css('li>a>div>p>strong.date::text').extract()

          MealType=sel.css('span.blue::text').extract()
          #sel.xpath('normalize-space(.//strong[@class="date"])').extract()
       
          for x in range(0,len(data)):
           IC[x]=''.join(map(str, IC[x]))
           
        


          ICn=[j.strip() for j in IC]



          for x in range(0,len(data)):
              Dates[x]=Dates[x].strip()
              yield{

              'HotelName': name,
              'Destination':"Kreta",
              'InviaCode':ICn[x],
              'Dates':Dates[x],
              'MealType':MealType[x],
              'Operator':Op[x].strip(),
              'Price':PR[x]
              }

        next_page = ag.css("a.next::attr(data-page)").extract_first()
        print("Page %s -1" %next_page)
        url = re.sub('page=\d+', 'page=' + next_page, response.url)
        yield scrapy.Request(url, self.logged_in)
