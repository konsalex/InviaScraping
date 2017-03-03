# -*- coding: cp1253 -*-
import scrapy
import re
from scrapy.selector import Selector
import json




f=open('dates.txt')           #������� �� ������
lines=f.readlines()        #�������� ��� �������
first=lines[0].split()      #����� split ���� ��������

print (first[0]+" "+first[1])



url_date1="https://dovolena.invia.cz/direct/tour_search/ajax-next-boxes/?nl_country_id%5B%5D=28&nl_locality_id%5B%5D=19&d_start_from="
url_date2=first[0]
url_date3="&d_end_to="
url_date4=first[1]
url_date5="&nl_length_int%5B%5D=7%7C9&nl_length_int%5B%5D=10%7C12&nl_length_int%5B%5D=13%7C&nl_transportation_id%5B%5D=3&sort=nl_sell&page=1&getOptionsCount=true&base_url=https%3A%2F%2Fdovolena.invia.cz%2F"
url_final=url_date1+url_date2+url_date3+url_date4+url_date5
print (url_final)


print (type(url_final))
