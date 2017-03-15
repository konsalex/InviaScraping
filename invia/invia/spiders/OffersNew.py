import scrapy
import re
from scrapy.selector import Selector
import json




class MySpider(scrapy.Spider):
    name = 'OffersNew'
    start_urls = ['https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999']
    download_delay = 0.5

    def start_requests(self):
        return [scrapy.FormRequest("https://www.invia.cz/direct/community_login/ajax-login/?ac_email=zisi%40electratours.cz&ac_password=electra1999",
                                   formdata={'user': '', 'pass': ''},
                                   callback=self.after_login)]


    def after_login(self, response):

            return scrapy.Request(url="https://dovolena.invia.cz/direct/tour_search/ajax-next-boxes/?d_start_from=14.03.2017&nl_ck_id%5B%5D=62&sort=nl_sell&page=1&getOptionsCount=true&base_url=https%3A%2F%2Fdovolena.invia.cz%2F",callback=self.logged_in)

    def logged_in(self, response):
        data=json.loads(response.text)
        if(data['error']==0):
          sel=Selector(text=data['boxes_html'])
        elif(data['error']!=1):
          request=scrapy.Request(url=response.url,callback=self.logged_in)
          yield request
          return 
        ag=Selector(text=data['boxes_html'])
        ko=sel.css('li.hotel-box').extract()

        for x in range(0,len(ko)):
          sel=Selector(text=ko[x])

          name=sel.css('span.name::text').extract_first()
	  
          data=sel.xpath('//li/@data-content-value').extract()

          IC=[json.loads(d)["nl_hotel_id"] for d in data]   
          
          Dest2=sel.css('div.wrap>div.content>p.location::text').extract()
          Dest=Dest2[1].strip().rsplit('\t', 1)[1] 

          
          for x in range(0,len(data)):
           IC[x]=''.join(map(str, IC[x]))

          ICn=[j.strip() for j in IC]

          
          url1="https://dovolena.invia.cz/direct/tour_search/ajax-next-box-rows/nl_hotel_id/"

          url2=ICn[x]

          url3="/?d_start_from=14.03.2017&nl_ck_id%5B%5D=62&sort=nl_sell&boxPage=1"

          url_final=url1+url2+url3

          print(url_final)

          request=scrapy.Request(url=str(url_final),callback=self.hotel)

          request.meta["name"]=name
          request.meta["invia"]=ICn[x]
          request.meta["dest"]=Dest

          yield request

        if(ag.css("a.next::attr(data-page)")):  
          next_page = ag.css("a.next::attr(data-page)").extract_first()
          print("Page %s -1" %next_page)
          url = re.sub('page=\d+', 'page=' + next_page, response.url)
          yield scrapy.Request(url, self.logged_in)

    def hotel(self,response):
      
      after=response.css('li').extract()
      names = response.meta['name']
      inviacode=response.meta["invia"]
      dest=response.meta["dest"]
      for x in xrange(0,len(after)):
        af=Selector(text=after[x])
        dates=af.css("strong.date::text").extract_first()
        prices=af.css("strong.orange").extract_first()
        airport=af.css("p.info>span::attr(title)").extract_first()
        meal=af.css("span.blue::text").extract_first()
        minute=af.css("span.symptom::text").extract_first()
        oper=af.css("div:nth-child(2)>p.r::text").extract_first()
        oper=oper.strip()
        dates=dates.strip()
        yield{
        "InviaCode":inviacode,
        "Operator":oper,
        "Hotel":names,
        "Dates":dates,
        "Airport":airport,
        "MealType":meal,
        "Minute":minute,
        "Destination":dest
        }


      if(response.css("a.next")):
        name=names
        next_page = response.css("a.next::attr(rel)").extract_first()
        url = re.sub('boxPage=\d+', 'boxPage=' + next_page, response.url)
        request=scrapy.Request(url,callback=self.hotel)
        request.meta["name"]=name
        request.meta["invia"]=inviacode
        yield request
      else:
        return
