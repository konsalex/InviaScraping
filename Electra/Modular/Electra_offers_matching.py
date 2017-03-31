# -*- coding: UTF-8 -*-
import xmltodict
import csv
import glob, os
import types
import sys;
import time
import re

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()





reload(sys);
sys.setdefaultencoding("utf8")




## Function to check similarity of the dates ##

def CheckDates(InvString, ElDep, ElArr):
    date=InvString.split("-")
    
    dep=date[0].split(".")
    
    arr=date[1].split(".")
    
    depday=int(dep[0])
    
    depmonth=int(dep[1])

    arrday=int(arr[0])
    
    armonth=int(arr[1])

    depel=ElDep.split("-")

    arrel=ElArr.split("-")
    
    depdayel=int(depel[2])

    depmonthel=int(depel[1])

    arrdayel=int(arrel[2])

    armonthel=int(arrel[1])

    if( depday==depdayel and depmonth==depmonthel and arrday==arrdayel and armonth==armonthel):
        return True

    return False
    


### Load Electra Offers ###

f=open('Electra_Offers.csv')
lines=f.readlines() 

ElectraName=[]
ElectraCode=[]
ElectraStart=[]
ElectraEnd=[]
ElectraAirport=[]
ElectraDest=[]
ElectraMeal=[]
ElectraPrice=[]

for x in xrange(1,len(lines)):
    temp=lines[x].split(",")
    print (len(temp))
   
    ElectraName.append(temp[0].encode("utf-8").strip())
    ElectraCode.append(temp[1].encode("utf-8").strip())
    ElectraStart.append(temp[2].encode("utf-8").strip())
    ElectraEnd.append(temp[3].encode("utf-8").strip())
    if(len(temp)==9):
        ElectraAirport.append(temp[4].encode("utf-8").strip().replace(","," "))
        ElectraDest.append(temp[5].decode("utf-8").strip())
        ElectraMeal.append(temp[6].decode("utf-8").strip())
        ElectraPrice.append(temp[7].decode("utf-8").strip())
    else:
        ElectraAirport.append(temp[4].encode("utf-8").strip().replace(","," "))
        ElectraDest.append(temp[6].decode("utf-8").strip())
        ElectraMeal.append(temp[7].decode("utf-8").strip())
        ElectraPrice.append(temp[8].decode("utf-8").strip())

del(f)

print(len(ElectraName))



### Open Database csv ###

f=open('Database.csv')
lines=f.readlines() 
OurCode=[]
InviaDataCode=[]

for x in xrange(1,len(lines)):
    temp=lines[x].split(",")
    OurCode.append(temp[1].encode("utf-8").strip())
    InviaDataCode.append(temp[3].encode("utf-8").strip())


### Initiate Extra column for CSV matching ###

InviaStatus=[]


### Load Invia Offers ###

f=open('Offers_Invia.csv') 
lines=f.readlines()
InviaDate=[]
InviaCode=[]
InviaAir=[]
InviaMeal=[]

for x in xrange(1,len(lines)):
    temp=lines[x].split(",")
    
    InviaDate.append(temp[0].decode("utf-8").strip())
    
    InviaCode.append(temp[2].strip().decode("utf-8"))
    
    InviaAir.append(temp[7].strip().decode("utf-8"))

    InviaMeal.append(temp[4].strip().decode("utf-8"))
    


### Start Searching one by one Electra offers and try to match them with Invia's ###

for x in xrange(0,len(ElectraName)):
        
    flag=0

    for y in xrange(0,len(OurCode)):
        if(ElectraCode[x]==OurCode[y]):
            tempcode=InviaDataCode[y]
            flag=1
            break
    
    if (flag==0):
        InviaStatus.append("No Invia Code")
        

    if(flag==1):
        for z in xrange(0,len(InviaCode)):
            if(tempcode==InviaCode[z]):
                ElectraAirport[x]=re.sub(r'"', '', ElectraAirport[x])
                
                if(InviaAir[z]==ElectraAirport[x]):

                    ##Checking the Dates ##
                    if(CheckDates(InviaDate[z],ElectraStart[x],ElectraEnd[x])):
                        
                        ## Checking The meal Type ##
                        if(similar(ElectraMeal[x],InviaMeal[z])>0.8):
                            
                            InviaDate.pop(z)
        
                            InviaCode.pop(z)
                            
                            InviaAir.pop(z)

                            InviaMeal.pop(z)

                            InviaStatus.append("There is an offer")
                            flag=2
                            break

    if(flag==1):
        InviaStatus.append("No Package")
        








### Append the results to finals CSV ###

with open('Electra_Offers_final.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(['Name','Code','Departure', 'Arrival', 'Airport','Destinaion','MealType','InviaStatus'])
    rows = zip(ElectraName,ElectraCode,ElectraStart,ElectraEnd,ElectraAirport,ElectraDest,ElectraMeal,InviaStatus)
    for row in rows:
        
        writer.writerow(row)
del(rows) 
del(f)   
    