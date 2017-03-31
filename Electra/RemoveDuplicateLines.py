from more_itertools import unique_everseen
with open('Electra_Offers.csv','r') as f, open('Test.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
