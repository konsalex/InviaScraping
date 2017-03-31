from difflib import SequenceMatcher
import csv
import sys
from compsim.company_name_similarity import CompanyNameSimilarity
import sys
import xmltodict
import glob, os
import requests
from xml.etree import ElementTree as ET
import urllib
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


reload(sys)
sys.setdefaultencoding("utf8")


### Load Invia Offers CSV and keep Unique Names,Codes,Dests ###


f=open('Offers_Invia.csv') 
lines=f.readlines()
InviaName=[0]
InviaCode=[0]
InviaDest=[0]
counter=1

for x in xrange(1,len(lines)):
    temp=lines[x].split(",")
    n=1
    for y in InviaCode:
        if((temp[2].decode("utf-8").strip())==y):
            n=0
    
    if(n==1):    
        
        InviaName.append(temp[5].decode("utf-8").strip())
        InviaCode.append(temp[2].strip().decode("utf-8"))
        InviaDest.append(temp[1].strip().decode("utf-8"))
        counter+=1
        print("success?")


InviaName.pop(0)
InviaCode.pop(0)
InviaDest.pop(0)

print(len(InviaCode))



### Clean All xml files in the Directory ###

files=[]
for file in glob.glob("*.xml"):
    files.append(file)

for fname in files:
    os.remove(fname)


### Load Electra Active xml ###

r = requests.get('http://www.electratours.cz/api/export/legacy/list?username=webco&password=webco123')

with open("output.xml", 'w'): pass   #empty previous output and erase the content

with open("output.xml", "w") as f:
    f.write(r.text.encode("utf-8"))   #writing active product xml to output.xml
del(f)

Codes=[]
Dest=[]
Name=[]

with open("output.xml") as f:
    doc = xmltodict.parse(f.read())
for x in xrange(0,len(doc['Export']['Zajezd'])):
    Codes.append(doc['Export']['Zajezd'][x]['@Kod'])
    Name.append(doc['Export']['Zajezd'][x]['@Nazev'])
    Dest.append(doc['Export']['Zajezd'][x]['Destinace']['Destinace']['Destinace']['Destinace']['Destinace']['@Nazev'])

del(f)
### Load Database Data ###

f=open('Database.csv')
lines=f.readlines() 
IDC=[]
for x in xrange(1,len(lines)):
    temp=lines[x].split(",")    
    IDC.append(temp[3].encode("utf-8").strip())               # InviaDatabaseCode
del(f)


### Open CSV for appending new entries ###

with open('Database.csv','ab') as w:
    writer=csv.writer(w)
    for x in xrange(0,len(InviaCode)):
        n=0
        for z in IDC:
            if(z==InviaCode[x]):
                n=1
                break
        if(n==0):
            for y in xrange(0,len(Name)):
                print(Dest[y] + "  " + InviaDest[x])
                if(similar(Dest[y],InviaDest[x])>0.65):
                    cm = CompanyNameSimilarity()
                    tempo=cm.match_score(Name[y], InviaName[x])
                    if(tempo>0.7):
                        row=zip([Name[y].replace("-"," ").title()],[Codes[y]],[InviaName[x]],[InviaCode[x]],[Dest[y]])
                        writer.writerows(row)
                        del(row)
                        n=1
                        break
        if(n==0):
            row=zip([""],[""],[InviaName[x]],[InviaCode[x]],[InviaDest[x]])
            writer.writerows(row)
            del(row)


### Download all Electra's offers xml(s) ###

url="http://www.electratours.cz/api/export/legacy/detail?username=webco&password=webco123&kod="

for t in Codes:
    urllib.urlretrieve(url+t, t+".xml")










"""
f=open('Electra_Offers_sketo2.csv') 
lines2=f.readlines()
ElectraName=[]
ElectraCode=[]
ElectraDest=[]


for x in xrange(1,len(lines2)):
    temp2=lines2[x].split(",")
    ElectraName.append(temp2[0].encode("utf-8"))
    ElectraCode.append(temp2[1].encode("utf-8"))
    ElectraDest.append(temp2[2].strip().decode("utf-8"))
    

OurName=[]
InviasName=[]
OurCode=[]
InviasCode=[]
Dest=[]

cm = CompanyNameSimilarity()
for y in xrange(0,len(InviaName)):
    for i in xrange(0,len(ElectraName)):    
        n=0
        if(similar(ElectraDest[i], InviaDest[y])>0.65):
	    print("Mpika")
            cm = CompanyNameSimilarity()
            tempo=cm.match_score(ElectraName[i], InviaName[y])
            if(tempo>0.7):
                print("oeeee")
                OurName.append(ElectraName[i].encode("utf-8"))
                InviasName.append(InviaName[y].encode("utf-8"))
                OurCode.append(ElectraCode[i].encode("utf-8"))
                InviasCode.append(InviaCode[y].encode("utf-8"))
                Dest.append(InviaDest[y].encode("utf-8"))
                n=1
                break
    if (n==0):
        OurName.append("")
        InviasName.append(InviaName[y].encode("utf-8"))
        OurCode.append("")
        InviasCode.append(InviaCode[y].encode("utf-8"))
        Dest.append(InviaDest[y].encode("utf-8"))
                
                
            
         
            
            
            
        

print(len(InviaName))
print(len(InviasCode))

with open('Comparing.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['OurName','OurCode','InvName', 'InvCode','Dest'])
    rows = zip(OurName,OurCode,InviasName,InviasCode,Dest)
    print(len(rows))
    for row in rows:
        writer.writerow(row)

"""
