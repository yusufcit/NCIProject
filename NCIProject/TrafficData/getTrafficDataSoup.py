# Import libraries
import csv
import datetime
import re
import requests
import os
from TrafficData import GetDownloadLinks


from DBConnect import DBConnection
from TrafficData.GetGeoLocations import addgeLocationData

def gatherTrafficData():
    currentDir = os.getcwd()
    print("The current working directory is %s" % currentDir)

    # define the name of the directory to be created
    location = "tmp/EVData/Traffic"
    path = os.path.join(currentDir, location)
    print("full path is : %s" % os.path.join(currentDir, path))

    ### Creating Directory based on current location
    try:
        os.makedirs(path, 0o777)
    except OSError:
        print("Directory %s failed to create" % path)
    else:
        print("Directory %s created" % path)
    os.chdir(path)
    fromDate = datetime.date(2017, 0o1, 0o1)
    toDate = datetime.datetime.now().date() - datetime.timedelta(1)

    urls = GetDownloadLinks.geturls(fromDate, toDate)

    iterator = 0
    # download the files in path
    for url in urls:
        iterator = iterator + 1
        os.chdir(path)
        workingDir = os.getcwd()
        print("The current working directory is ", workingDir)
        response = requests.get(url)
        print("url content is: " + url)
        open('file%s' % iterator + '.csv', 'wb').write(response.content)

    ###################################################################
    ####################### Reading in the files and adding to DB ###########

    ## Connecting to DB and inserting data
    conn = DBConnection.DBConnection.connect_dbs()
    cursor = conn.cursor()

    #### Creating table if does not exist ####
    createTable = "CREATE TABLE IF NOT EXISTS trafficdata (cosit varchar(255), " \
                  "class int, year int, month int, day int, vehiclecount int, " \
                  "geolocation varchar(255),description varchar(255))"
    try:
        cursor.execute(createTable)
        conn.commit()
    except:
        print("Failed to create table")

    # Find non digit in cells
    def find_non_digit(row):
        for x in row:
            if re.findall('\D', x):
                return True

    # Reading the csv file and inserting to DB
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                with open(file) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            print(f'Column names are {", ".join(row)}')
                            line_count += 1
                        elif find_non_digit(row):
                            print("Unwanted data found")
                        else:
                            print("Inserting following to DB: ", row)
                            try:
                                vale = (row[0], row[1], row[2], row[3], row[4], row[5])
                                cursor.execute(
                                    "INSERT INTO TrafficData (cosit, class, year, month, day,VehicleCount) VALUES (%s, %s, %s, %s, %s, %s)",
                                    vale)
                                count = cursor.rowcount
                                print("number of raw effected: ", count)
                                conn.commit()
                                print("Following value is inserted to DB: ", row)
                            except:
                                print("Failed to add following to DB: ", vale)

    cursor.close()

    addgeLocationData()

    os.chdir(currentDir)
