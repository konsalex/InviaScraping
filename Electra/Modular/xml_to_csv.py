# -*- coding: cp1253 -*-
import xmltodict
import csv
import glob, os
import types
import sys
import xml.etree.ElementTree as ET


reload(sys)
sys.setdefaultencoding("utf8")

### Remove Output.xml for not included in glob xml files ###

if os.path.isfile("output.xml"):
    os.remove("output.xml")
    print("Output.xml removed")
else:
    print("No output.xml")


### Open Electra_Offers.csv and parse all xml results inside ###

with open('Electra_Offers.csv', 'wb') as f:
    writer = csv.writer(f)
    test=1
    writer.writerow(['Name','Code','Departure', 'Arrival', 'Airport','Destinaion','MealType','Price'])
    files=[]
    for file in glob.glob("*.xml"):
        files.append(file)
    for fname in files:
        with open(fname) as fd:
            doc = xmltodict.parse(fd.read())
            Names=doc['Export']['Zajezd']['@Nazev']

            Codes=doc['Export']['Zajezd']['@Kod']
            Dest=doc['Export']['Zajezd']['Destinace']['Destinace']['Destinace']['Destinace']['Destinace']['@Nazev']
            StartDate=[]
            EndDate=[]
            Airport=[]
            Name=[]
            Code=[]
            Destination=[]
            Price=[]
            Meal=[]
            test+=1
            types=[]
            str1=''.join(doc['Export']['Zajezd']['Cenik'])
            
            if 'Termin' in str1 :
                if isinstance(doc['Export']['Zajezd']['Cenik']['Termin'],list):
                        
                        for x in xrange(0,len(doc['Export']['Zajezd']['Cenik']['Termin'])):
                            
                            
                            if(len(doc['Export']['Zajezd']['Cenik']['Termin'][x])>11):
                                


                                if(len(doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena'])>30):
                                    
                                    if((doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena']['@Nazev']).encode("utf8")=="Dospělý na pevném lůžku"):

                                        StartDate.append(doc["Export"]["Zajezd"]["Cenik"]["Termin"][x]["@TerminOd"].encode('utf-8').strip())
                                        
                                        EndDate.append(doc["Export"]["Zajezd"]["Cenik"]["Termin"][x]["@TerminDo"].encode('utf-8').strip())
                                         

                                        str=''.join(doc['Export']['Zajezd']['Cenik']["Termin"][x])
                                        if '@NavratovaStanice' in str:
                                            Airport.append(doc['Export']['Zajezd']['Cenik']['Termin'][x]['@NavratovaStanice'].encode('utf-8').strip())
                                        else:
                                            Airport.append("No airport")
                                           
                                        Name.append(Names.title().replace("-"," "))
                                        Code.append(Codes)
                                        Destination.append(Dest)
                                        
                                        Price.append((doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena']['@Cena']).encode('utf-8'))
                                        Meal.append((doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena']['@Strava']).encode('utf-8'))


                                else:

                                    for y in xrange(0,len(doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena'])):
                                        
                                        

                                        if((doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena'][y]['@Nazev']).encode("utf8")=="Dospělý na pevném lůžku"):

                                            if(doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena'][y]['@StravaKod'] not in types):
                                                StartDate.append(doc["Export"]["Zajezd"]["Cenik"]["Termin"][x]["@TerminOd"].encode('utf-8').strip())
                                                
                                                EndDate.append(doc["Export"]["Zajezd"]["Cenik"]["Termin"][x]["@TerminDo"].encode('utf-8').strip())
                                                 

                                                str=''.join(doc['Export']['Zajezd']['Cenik']["Termin"][x])
                                                if '@NavratovaStanice' in str:
                                                    Airport.append(doc['Export']['Zajezd']['Cenik']['Termin'][x]['@NavratovaStanice'].encode('utf-8').strip())
                                                else:
                                                    Airport.append("No airport")
                                                   
                                                Name.append(Names.title().replace("-"," "))
                                                Code.append(Codes)
                                                Destination.append(Dest)
                                                
                                                Price.append((doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena'][y]['@Cena']).encode('utf-8'))
                                                Meal.append((doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena'][y]['@Strava']).encode('utf-8'))
                                                types.append(doc['Export']['Zajezd']['Cenik']['Termin'][x]['Cena'][y]['@StravaKod'])

                                            else:
                                                break

                                    del types[:]

                    
        rows = zip(Name,Code,StartDate,EndDate,Airport,Destination,Meal,Price)
                
        for row in rows:
            writer.writerow(row)
        del(rows)
        del(doc)




###  Remove all xml files from folder ###

for fname in files:
    os.remove(fname)
    print( fname + "removed")
