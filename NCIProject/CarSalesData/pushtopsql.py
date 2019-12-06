#https://www.dataquest.io/blog/loading-data-into-postgres/

#import csv
import psycopg2

#the below is to log into our database
conn = psycopg2.connect("host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")
cur = conn.cursor()
 
#the below is to create a new table
cur.execute("""
CREATE TABLE registrations (
RegistrationID int, 
Year int,
Month varchar(30), 
County varchar(50), 
RegistrationType varchar(255),
EngineType varchar(255),
CarRegistrationCount int)
""") 

#this is to copy the data from the csv file and to paste it into the table that was created above
with open('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\passengercarmediafire\\passengercars.csv', 'r') as f:
    next(f) # Skip the header row.
    cur.copy_from(f, 'registrations', sep=',') 

#the below is to confirm the table created and to update our data warehouse
conn.commit()
