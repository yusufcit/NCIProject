import folium
import psycopg2
import pandas as pd
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

fg= folium.FeatureGroup(name='Car traffic by road')

def generateBaseMap(default_location=[53.547946, -7.716734], default_zoom_start=7):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

df_copy = df.copy()

df_day_list = []

for day in df_copy.day.sort_values().unique():
    df_day_list.append(df_copy.loc[df_copy.day == day, ['longitude', 'latitude', 'count']].groupby(['longitude', 'latitude']).sum().reset_index().values.tolist())

base_map = generateBaseMap()

HeatMap(data=df_copy[['longitude','latitude','vehiclecount']].groupby(['longitude','latitude']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(base_map)
HeatMapWithTime(df_day_list, radius=1, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(base_map)

base_map.save("Traffic_by_road.html")