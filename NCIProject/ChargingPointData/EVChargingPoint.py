# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:55:32 2019

@author: dotsi
"""
# Import libraries
import requests
import psycopg2
import time
import zipfile, io
import os
from bs4 import BeautifulSoup
import shutil

def getChargingPointData():

    currentDir = os.getcwd()
    print("The current working directory is %s" % currentDir)

    # define the name of the directory to be created
    location = "tmp/EVData/CPData"
    path = os.path.join(currentDir, location)
    print("full path is : %s" % os.path.join(currentDir, path))

    # Test for the successful creation of the directory to download the zip files
    try:
        os.mkdir(path, 0o777)
    except OSError:
        print("Directory %s failed to create" % path)
    else:
        print("Directory %s created" % path)

    # Define URL to extract data files from
    url = 'http://www.cpinfo.ie/data/archive.html'
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.content, "html.parser")
    # Call link from URL "a" tag #3; soup.findAll facilitates this check..

    for i in range(3, len(soup.findAll('a')) + 1):
        # print("value of i is: ", i)
        a_zip = soup.findAll('a')[i - 1]  # after the 2nd a, the next a tag is the link name
        ziplink = a_zip['href']  # convert the a ref to an actual web link
        pass_ziplink = requests.get(ziplink)
        zip = zipfile.ZipFile(io.BytesIO(pass_ziplink.content))  # zipfile library to extract source data
        zip.extractall(path)  # extract to specified location...should this be Github?
        time.sleep(2)  # pause the code for 2 times to avoid use of server side resources
        print("Name of zip Exported: ", ziplink)
    print('All zip files from ' + url + 'are saved to the folder ' + path + '.')

    # Connect to the PostgreSQL database server
    postgresConnection = psycopg2.connect(
        "dbname=ev_ireland user=nciadmin@nciproject password='Nciproject01?' host=nciproject.postgres.database.azure.com port=5432")
    # Get cursor object from the database connection
    cursor = postgresConnection.cursor()
    # Create table criteria
    Table = "EVCharge"
    sqlCreateTable = "create table " + Table + "(recorddate text, daytime text, chargepointid text, chargepointtype text, status text, coord text, address text, longitude text, latitude text);"
    cursor.execute(sqlCreateTable)
    postgresConnection.commit()
    # Get the updated list of tables
    sqlGetTableList = "SELECT table_schema,table_name FROM information_schema.tables where table_schema='test' ORDER BY table_schema,table_name ;"
    # Retrieve all the rows from the cursor
    cursor.execute(sqlGetTableList)
    tables = cursor.fetchall()

    # define the path and listing of files to be transferred
    directory_listing = os.listdir(path)
    print(os.listdir(path))  # all names of the files in the directory

    # Traverse the directory 'path' in order to get the files written to the table EVCharge
    os.chdir(path)
    for (r, d, f) in os.walk(path):
        for file in f:
            with open(file) as d:
                cursor.copy_from(d, 'EVChargetext')
                postgresConnection.commit()
    cursor.close()
    postgresConnection.close()

    print('')
    print("All files from directory " + path + " directory written to the table " + Table)

    # Final: delete directory all data files had been saved to
    try:
        shutil.rmtree(path)
    except:
        print("Files deleted")
