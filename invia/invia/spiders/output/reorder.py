import csv

with open('Kreta.csv', 'r') as infile, open('Kretaordered.csv', 'a') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['Destination', 'InviaCode', 'HotelName', 'Dates', 'MealType','Operator','Price']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)

with open('Corfu.csv', 'r') as infile, open('Corfuordered.csv', 'a') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['Destination', 'InviaCode', 'HotelName', 'Dates', 'MealType','Operator','Price']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)

with open('Zakynthos.csv', 'r') as infile, open('Zakynthosordered.csv', 'a') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['Destination', 'InviaCode', 'HotelName', 'Dates', 'MealType','Operator','Price']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)


with open('Rhodos.csv', 'r') as infile, open('Rhodosordered.csv', 'a') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['Destination', 'InviaCode', 'HotelName', 'Dates', 'MealType','Operator','Price']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)

