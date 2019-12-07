import requests

import DBConnection

def addgeLocationData():
    url = "https://data.tii.ie/Datasets/TrafficCountData/sites/tmu-sites.json"
    data = []
    try:
        response = requests.get(url)
        data = response.json()
    except:
        print("Failed to load geo location json file")

        ## Connecting to DB and inserting data
    conn = DBConnection.DBConnection.connect_dbs()
    cursor = conn.cursor()

    query = "UPDATE TrafficData SET geolocation = '{}', description = '{}' WHERE cosit = '{}'"
    if data.__sizeof__() > 0:
        for d in data:
            cosit = (d["cosit"])
            cositTrimmed = (d["cosit"].lstrip("0"))
            description = (d["description"]).replace("'", "`")
            location = (d["location"])
            latlang = str(location["lat"]) + "," + str(location["lng"])
            try:
                cursor.execute(query.format(latlang, description, cositTrimmed))
                cursor.execute(query.format(latlang, description, cosit))
                count = cursor.rowcount
                print("number of raw effected: %s", count)
                conn.commit()
            except:
                print("Failed to add following to DB: %s %s ", latlang, description)

            print(cosit)
            print(latlang)
    else:
        print("No data found on the link: %s", url)

    cursor.close()






