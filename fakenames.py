from faker import Faker
import csv
from random import randrange
from random import randint 
import pandas as pd
import requests
import json
import string
import random

#random_age = round(random.uniform(18.0, 70.0), 1)
values = randint(0,1000000)
#print(values)
 
# Randomly choose a letter from all the ascii_letters
randomLetter = random.choice(string.ascii_letters)
#print(randomLetter)
ppsn = (str(values)+randomLetter)

def html():
    fake = Faker()

    #fake.name()

    for i in range(0,10):
        print(i,fake.name())

    
#https://www.echolive.ie/corknews/arid-41364103.html
#532 adults accessed emergency accommodation in Cork
    with open('fakenames.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'Name','Age', 'PPSN'])
        for n in range(1, 533):
            values = randint(1000000,9999999)
            randomLetter = random.choice(string.ascii_letters)
            ppsn = (str(values)+randomLetter)
            writer.writerow((n,fake.name(), randrange(18,70),ppsn))
            
    a = pd.read_csv("fakenames.csv",index_col=False) 
    # to save as html file 
    # named as "Table" 
    a.to_html("fakenames.html",index=False) 
    # assign it to a  
    # variable (string) 
    html_file = a.to_html()

if __name__ == "__main__":
    html()