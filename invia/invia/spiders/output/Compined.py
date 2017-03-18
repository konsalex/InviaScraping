import glob
import os


interesting_files = glob.glob("*.csv") 

header_saved = False
with open('compined.csv','wb') as fout:
    for filename in interesting_files:
        with open(filename) as fin:
            header = next(fin)
            if not header_saved:
                fout.write(header)
                header_saved = True
            for line in fin:
                fout.write(line)


os.remove("Corfu.csv")
os.remove("Kreta.csv")
os.remove("Corfuordered.csv")
os.remove("Kretaordered.csv")
os.remove("Rhodos.csv")
os.remove("Rhodosordered.csv")
os.remove("Zakynthos.csv")
os.remove("Zakynthosordered.csv")


