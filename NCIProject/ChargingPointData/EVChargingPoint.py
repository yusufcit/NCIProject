# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:55:32 2019

@author: David O' Reilly
"""
# Import libraries
import requests
import psycopg2
import time
import zipfile, io
import os
from bs4 import BeautifulSoup

def getChargingPointData():
    # 1. Create directory and test for the successful creation in order to download the zip files
    # define the name of the directory to be created to store the data
    currentDir = os.getcwd()
    print("The current working directory is %s" % currentDir)

    # define the name of the directory to be created
    location = "tmp/EVData/chargingPoint"
    path = os.path.join(currentDir, location)
    print("full path is : ", path)

    try:
        os.mkdir(path, 0o777)
    except OSError:
        print("Directory %s failed to create" % path)
    else:
        print("Directory %s created" % path)

    # 2. Table creation: Connect to the PostgreSQL database server,
    postgresConnection = psycopg2.connect(
        "dbname=ev_ireland user=nciadmin@nciproject password='Nciproject01?' host=nciproject.postgres.database.azure.com port=5432")
    # Get cursor object from the database connection
    cursor = postgresConnection.cursor()

    # Create on the DB "evchargetext" table template and colums to store all the zip file data downloaded
    Table = "evchargetext"
    sqlCreateTable = "CREATE TABLE IF NOT EXISTS" + Table + "(recorddate text, daytime text, chargepointid text, chargepointtype text, status text, coord text, address text, longitude text, latitude text);"
    cursor.execute(sqlCreateTable)
    postgresConnection.commit()

    # Create on the DB "CPtable" table template and columns - chargepoint types
    TableCPType = "CPType"
    sqlCreateTableCPType = "CREATE TABLE IF NOT EXISTS" + TableCPType + "(Code text, Detail text);"
    cursor.execute(sqlCreateTableCPType)
    postgresConnection.commit()
    # Load CPtable data - used to facilitate the clean up of inconsistent data via SQL queries at end of this script
    insertStatement = "insert into cptype (Code, detail) VALUES ('NA', 'NA org data files'), ('Services', 'General Services'), ('StandardType2', 'Standard Version 2'), ('CHAdeMO', 'Moving Use Charge'), ('ComboCCS', 'Combined Charging System'), ('FastAC43', 'Rapid Charge')";
    cursor.execute(insertStatement);
    postgresConnection.commit()

    # Create on DB "CPStatus" table template and columns- chargepoint status
    TableStatus = "CPStatus"
    sqlCreateTablestat = "CREATE TABLE IF NOT EXISTS" + TableStatus + "(StatusCode text, StatusDetail text);"
    cursor.execute(sqlCreateTablestat)
    postgresConnection.commit()
    # Load CPtable data - used to facilitate the clean up of inconsistent data via SQL queries at end of this script
    insertStatementstat = "insert into cpstatus (StatusCode, StatusDetail) VALUES ('OOS', 'Out of Service'), ('OOC', 'Out of Contact'), ('Part', 'Partially Occupied'), ('Occ', 'Fully Occupied'), ('Unknown','Unknown status')";
    cursor.execute(insertStatementstat);
    postgresConnection.commit()

    # 3. Extract the data from cpinfo, looping through all a refs
    # Inform the user of status at end of each zip extraction

    # Define URL to extract data files from
    url = 'http://www.cpinfo.ie/data/archive.html'

    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.content, "html.parser")
    # Call link from URL "a" tag #3 as 3 is the first ref of the zip drive. Iterate through the page returning all A hrefs
    # soup.findAll facilitates this check..
    for i in range(3, len(soup.findAll('a')) + 1):
        a_zip = soup.findAll('a')[i - 1]  # after the 2nd a, the next a tag is the link name
        ziplink = a_zip['href']  # convert the a ref to an actual web link
        pass_ziplink = requests.get(ziplink)
        zip = zipfile.ZipFile(io.BytesIO(pass_ziplink.content))  # zipfile library to extract source data
        zip.extractall(path)  # extract data to specified location...
        time.sleep(2)  # pause the code for 2 times to avoid use of server side resources
        print("Name of zip Exported: ", ziplink)
    print("")
    print('All zip files from ' + url + ' are saved to the folder ' + path + '.')

    # Get the updated list of tables
    sqlGetTableList = "SELECT table_schema,table_name FROM information_schema.tables where table_schema='test' ORDER BY table_schema,table_name ;"
    # Retrieve all the rows from the cursor
    cursor.execute(sqlGetTableList)
    tables = cursor.fetchall()

    # 4. Advise the user of the files to transfer
    directory_listing = os.listdir(path)
    print("List of all files to be written to DB:")
    print(os.listdir(path))

    # 5. Go to the directory the files are saved down, traverse the file listing and transfer the file to the table evchargetext
    os.chdir(path)
    for (r, d, f) in os.walk(path):
        for file in f:
            with open(file, 'r') as d:
                cursor.copy_from(d, 'evchargetext')
                postgresConnection.commit()
                print(
                    "Complete: " + file + " was copied to DB.")  # Tell the user the file x has been transferred successfully

    # 5. Clean up data on the targeted columns of evchargetext table in order to use to build graphs
    # Cleanse the Status of evchargetext table
    # If status code is not on the table cpstatus, give status on EVChargetext "No Status Available"; advise user SQL completed
    updateStatusStatement = (
        "UPDATE evchargetext SET status = 'No Status Available' WHERE NOT EXISTS (SELECT 1 FROM cpstatus WHERE cpstatus.statuscode = evchargetext.status)");
    cursor.execute(updateStatusStatement)
    postgresConnection.commit()
    print("Completed: Status clean up")

    # If status chargepointtype is not on the table cptype, give cptype on EVChargetext "Unattainable"; advise user SQL completed
    updateCPTypeStatement = (
        "UPDATE evchargetext SET chargepointtype = 'Unattainable' WHERE NOT EXISTS (SELECT 1 FROM cptype WHERE cptype.code = evchargetext.chargepointtype)");
    cursor.execute(updateCPTypeStatement)
    postgresConnection.commit()
    print("Completed: Chargepointtype clean up")

    # Cleanse the RecordDate of evchargetext table between Nov-16 to Jul-19; advise user SQL completed
    updateDateStatement = (
        "UPDATE evchargetext SET recorddate = 'No date..' WHERE evchargetext.recorddate LIKE '%CP%' OR evchargetext.recorddate LIKE '%,%' OR evchargetext.recorddate LIKE '%Unknown%' OR evchargetext.recorddate LIKE '%available%' OR CAST(evchargetext.recorddate AS INTEGER) < '20161031' OR CAST(evchargetext.recorddate AS INTEGER) > '20190801'");
    # UPDATE evchargetext SET recorddate = 'No date available' WHERE CAST(evchargetext.recorddate AS INTEGER) < '20161031' OR CAST(evchargetext.recorddate AS INTEGER) > '20190801'");
    cursor.execute(updateDateStatement)
    postgresConnection.commit()
    print("Completed: Date cleanup")

    # 6. Close the cursor and connection to the DB
    cursor.close()
    postgresConnection.close()

    # 7. Advise the user the script has transferred all data to the named table.
    print('')
    print("All files from directory " + path + " directory written to the table " + Table)

    os.chdir(currentDir)

    # 8. Delete all data files that have been downloaded in order to free up memory
    try:
        os.removedirs(path)
    except:
        print("Failed to delete files!!")
