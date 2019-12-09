#https://towardsdatascience.com/data-101s-spatial-visualizations-and-analysis-in-python-with-folium-39730da2adf

import psycopg2
import pandas as pd
import folium
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime

#the below is to log into our database
conn = psycopg2.connect("host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

#SQL query
sql = ('''select 
a1.cosit, 
a1.description,
left(a1.geolocation,position(',' in a1.geolocation)-1) as longitude, 
right(a1.geolocation,length(a1.geolocation)-position(',' in a1.geolocation)) as latitude,
a1.day, 
sum(a1.vehiclecount) as vehiclecount 

FROM public.trafficdata a1

GROUP BY
a1.cosit, 
a1.description,
left(a1.geolocation,position(',' in a1.geolocation)-1), 
right(a1.geolocation,length(a1.geolocation)-position(',' in a1.geolocation)),
a1.day''')

#put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
df = pd.read_sql_query(sql,conn)

traffic_map = folium.Map(location=[53.547946, -7.716734], zoom_start=5,control_scale = True)

fg= folium.FeatureGroup(name='Car traffic by road')

for records in range(len(df['cosit'])+1):
    fg.add_child(folium.Marker(location=[df.iloc[records][2], df.iloc[records][3]],popup=df.iloc[records], icon=folium.Icon(color='green')))
    traffic_map.add_child(fg)

traffic_map.save("Traffic_by_road.html")