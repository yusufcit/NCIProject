import os
import psycopg2

def insertIntoDB():
    # the below is to log into our database
    conn = psycopg2.connect(
        "host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")
    cur = conn.cursor()

    # the below is to create a new table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
    RegistrationID int, 
    Year int,
    Month varchar(30), 
    County varchar(50), 
    RegistrationType varchar(255),
    EngineType varchar(255),
    CarRegistrationCount int)
    """)

    ################################### setting up path #############################################
    # this is to copy the data from the csv file and to paste it into the table that was created above
    currentDir = os.getcwd()
    print("The current working directory is %s" % currentDir)

    ### Including the file ###
    filePath = os.path.join(currentDir, "passengercars.csv")
    print("Full file path is: ", filePath)

    ################################################## Finished path setup ########################

    with open(filePath, 'r') as f:
        next(f)  # Skip the header row.
        print("Inserting following to DB: ", f.name)
        cur.copy_from(f, 'registrations', sep=',')

        # the below is to confirm the table created and to update our data warehouse
    conn.commit()


