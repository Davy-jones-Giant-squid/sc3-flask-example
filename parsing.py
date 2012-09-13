import sys, os
from bs4 import BeautifulSoup
import urllib2
import csv
import xlwt
import logging
from decimal import Decimal
from datetime import datetime
import datetime

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s', stream=sys.stderr)

data = open(os.path.join(os.path.dirname(__file__), 'data', 'chicago-birthrates-1999-2009.csv'), 'r')
wiki_link = 'http://en.wikipedia.org/wiki/%s'

mapping = {
    
    'Name': 0,
    'Summary': 1,
    
}

items = {}

book = xlwt.Workbook()
sheet = book.add_sheet('Chicago Areas Summary')
for elem in mapping.keys():
    sheet.write(0, mapping[elem], elem) 
linkList=[]

rank = 1
for row in csv.DictReader(data):
    raw_name = str(row['Community Area Name'])
    for elem in mapping.keys():
            items[elem] = ''
    
    if ' ' in raw_name:
        if raw_name[-1] == ' ':
            temp_name = raw_name.replace(" ", '')
            new_name = temp_name.replace(temp_name[1:], temp_name[1:].lower())
            linkList.append(wiki_link % new_name+ ',_Chicago')

        elif raw_name == 'MCKINLEY PARK':
            new_name = raw_name.replace ('MCKINLEY PARK','McKinley_Park')
            linkList.append(wiki_link % new_name+ ',_Chicago')
           
        else:
            temp_name = (raw_name.replace(' ','_'))
            list_index = []
            i = -1
            try:
                while 1:                    
                    i = temp_name.index('_', i+1)
                    list_index.append(i)        
            except ValueError:
                pass
        
            if len(list_index) == 2:
                line1 = temp_name[0]+ temp_name[1:list_index[0]+1].lower()
                line2 = temp_name[list_index[0]+1] + temp_name[list_index[0]+2:list_index[1]+1].lower()
                line3 = temp_name[list_index[1]+1] + temp_name[list_index[1]+2:].lower()
                new_name = line1 + line2 + line3
                linkList.append(wiki_link % new_name+ ',_Chicago')
                
            else:
                line1 = temp_name[0]+ temp_name[1:list_index[0]+1].lower()
                line2 = temp_name[list_index[0]+1] + temp_name[list_index[0]+2:].lower()
                new_name = line1 + line2             
                linkList.append(wiki_link % new_name+ ',_Chicago')

    sheet.write(rank, 0, raw_name)
    rank += 1


rank = 1
for link in linkList:
    print "Opening link %s" % link
    for elem in mapping.keys():
            items[elem] = ''
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    infile = opener.open(link)
    page = infile.read()
    soup = BeautifulSoup(page)
    summaries = soup.find("p")
    summary = summaries.get_text() 
    sheet.write(rank, 1, summary)
    rank +=1
    

data_dir = '/Users/sabine/Desktop/' 

filename = data_dir + 'Chicago Areas Summary' + str(datetime.date.today().year) + \
    str(datetime.date.today().month) + str(datetime.date.today().day) +'.xls' 

logging.info('Saving file as %s' % filename)
book.save(filename)
logging.info("Successfully saved file.")


    



   

