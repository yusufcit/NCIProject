import os

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ChargingPointCountByYear():
    try:
        # the below is to log into our database
        conn = psycopg2.connect(
            "host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

        # SQL query
        sql = ('''select 

            a1.year, 
            count(a1.chargepointid) as charging_point_counts

            from (select distinct 
            left(a2.recorddate,4) as year, 
            a2.chargepointid
            from public.evcharge a2
            where a2.chargepointtype in ('ComboCCS','FastAC43','CHAdeMO','StandardType2')
            ) a1

            group by 1''')

        # put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
        df = pd.read_sql_query(sql, conn)

        # Number of bars to be created
        y_pos = np.arange(len(df['year']))

        # Create bars
        plt.bar(y_pos, df['charging_point_counts'])

        # Create names on the x-axis
        plt.xticks(y_pos, df['year'])

        # Add axis
        plt.title('Charging points count by year')
        plt.ylabel('Charging points count')
        plt.xlabel('Year')

        # saving the figure as png
        fig1 = plt.gcf()
        plt.draw()
        if not os.path.exists("graphImages"):
            os.mkdir("graphImages")
        fig1.savefig("graphImages/Charging_points_count_by_year.png", dpi=100)

    except:
        print("Failed to save graph into the local drive")

