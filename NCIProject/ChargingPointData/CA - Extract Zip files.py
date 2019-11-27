# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:55:32 2019

@author: dotsi
"""
# Import libraries
import requests
#import urllib.request #not requierd as part of final code
import time
import zipfile, io
import os
from bs4 import BeautifulSoup

# define the name of the directory to be created
path = "C:/Users/dotsi/Desktop/EVData"
#Test for the successful creation of the directory
try:
    os.mkdir(path)
except OSError:
    print ("Directory %s failed to create" % path)
else:
    print ("Directory %s created" % path)

#Define URL to webscrape data files from
url = 'http://www.cpinfo.ie/data/archive.html'
# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object
soup = BeautifulSoup(response.content, "html.parser")

#List all URLs on the website, determines what min number on range loop below
#soup.findAll('a')

#To download the data sets, call link from URL A tag #3; soup.findAll facilitates this check..
#loop goes from a range being  #3 a ref link to the last a link ref (Start at 0), 
#each iteration +1 to the range, therefore traversing to the next link

for i in range(2,len(soup.findAll('a'))+1): #'a' tags are for links
    #while i != 0: #while the a_zip has a value not null, go through the loop'''
    a_zip = soup.findAll('a')[i] #after the 2nd a, the next a tag is the link name 
    #print("a_zip: ", a_zip) # test to ensure each a ref in the loop is collected...
    ziplink = a_zip['href'] # convert the a ref to an actual web link    
    pass_ziplink = requests.get(ziplink)
    #urllib.request.urlretrieve(ziplink) 
    print("Name of zip Exported: ", ziplink) # test to ensure each a ref in the loop is collected...
    zip = zipfile.ZipFile(io.BytesIO(pass_ziplink.content)) #zipfile library to extract source data
    zip.extractall(path) #extract to specified location...should this be Github? 
    '''Next steps: with the downloaded file, transfer to SQL or equivalent - ETL applied here
       When the transfer is completed (need any verification?), delete this file in order to free up data
       Advise user the data file was deleted.... 
    '''
    time.sleep(2) #pause the code for 2 times to avoid use of server side resources
else: #Confirm when all files from the page are downloaded
    print('All zip files from ' + url + 'are saved to the folder ' + path +'.')

'''
1.When all files are extracted, create a single CSV with the contents of this 
file being all files in the folder
2.Delete all the files originally downloaded to the drive?
3.This CSV is then transferred to the database / cleaned up...

4. Create error handling such that if the files are removed, then give message
...these files have moved...disaster for the output!!!
5. Should the host be informed of our scraping by way of header?
'''