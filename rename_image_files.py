import os
import csv

# Open the state_combinations CSV file
with open('state_combinations.csv','r', encoding='utf8') as file:
    csv_reader = csv.reader(file)
# with open('state_combinations.csv','r') as file:
#     csv_reader = csv.reader(file)
    sku = None
    # Iterate over each row in the CSV file
    for row in csv_reader:
        sku = row[2]
        print(row)

img_dir = 'state_combinations_1/images_1'
#print list of files in the directory
print(sorted(os.listdir(img_dir)))

#iterate over each file in the directory and rename the file to correspond with the SKU in the CSV file
for file in os.listdir(img_dir):
    os.rename(file, sku + '.png')

# change each file name in the images_ folder to the SKU in the CSV file the sku will be in the row that equals filename +1
for file in os.listdir(img_dir):
    os.rename(file, sku + '.png')

#close csv file
file.close()