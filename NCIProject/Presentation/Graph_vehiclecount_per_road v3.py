#https://python-graph-gallery.com/bubble-map/
#https://github.com/python-visualization/folium/issues/528
#https://stackoverflow.com/questions/37466683/create-a-legend-on-a-folium-map
#https://stackoverflow.com/questions/47163728/how-to-add-legend-gradient-in-folium-heat-map

import folium
import psycopg2
import pandas as pd
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime

#the below is to log into our database
conn = psycopg2.connect("host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

#SQL query
sql_traffic = ('''select 
a1.cosit, 
a1.description,
left(a1.geolocation,position(',' in a1.geolocation)-1) as longitude, 
right(a1.geolocation,length(a1.geolocation)-position(',' in a1.geolocation)) as latitude,
a1.day, 
sum(a1.vehiclecount) as vehiclecount 
FROM public.trafficdata a1
GROUP BY 1,2,3,4,5''')

sql_registered_cars = ('''
select 
a1.county, 
CASE a1.county
when 'Carlow' then '52.840833'
when 'Cavan' then '53.9897'
when 'Clare' then '52.9045'
when 'Cork' then 51.898611
when 'Donegal' then 54.65
when 'Dublin' then 53.333056
when 'Galway' then 53.271944
when 'Kerry' then 52.1545
when 'Kildare' then 53.1589
when 'Kilkenny' then 52.654167
when 'Laois' then 52.9943
when 'Leitrim' then 54.1247
when 'Limerick' then 52.664722
when 'Longford' then 53.733333
when 'Louth' then 53.9508
when 'Mayo' then 53.933260
when 'Meath' then 53.6055
when 'Monaghan' then 54.25
when 'Offaly' then 53.2357
when 'Roscommon' then 53.6276
when 'Sligo' then 54.266667
when 'Tipperary' then 52.4738
when 'Waterford' then 52.258333
when 'Westmeath' then 53.5345
when 'Wexford' then 52.334167
when 'Wicklow' then 52.975
END as latitude, 
CASE a1.county
when 'Carlow' then -6.926111
when 'Cavan' then -7.3633
when 'Clare' then -8.9811
when 'Cork' then -8.495833
when 'Donegal' then -8.116667
when 'Dublin' then -6.248889
when 'Galway' then -9.048889
when 'Kerry' then -9.5669
when 'Kildare' then -6.9096
when 'Kilkenny' then -7.252222
when 'Laois' then -7.3323
when 'Leitrim' then -8.002
when 'Limerick' then -8.623056
when 'Longford' then -7.8
when 'Louth' then -6.5406
when 'Mayo' then -9.4289
when 'Meath' then -6.6564
when 'Monaghan' then -6.966667
when 'Offaly' then -7.7122
when 'Roscommon' then -8.1891
when 'Sligo' then -8.483333
when 'Tipperary' then -8.1619
when 'Waterford' then -7.111944
when 'Westmeath' then -7.4653
when 'Wexford' then -6.4575
when 'Wicklow' then -6.049444
END as longitude, 
sum(a1.carregistrationcount) as ev_hv_count 
from public.registrations a1 
where a1.enginetype in ('Electric','Hybrid')
group by 1,2,3
''')

sql_charging_station = ('''
select distinct 
a1.address, 
a1.longitude, 
a1.latitude 
from public.evchargetext a1
inner join (select distinct 
			a2.address, 
			max(a2.recorddate),
			max(a2.daytime) 
			FROM public.evchargetext a2
			where a2.chargepointtype in ('ComboCCS','FastAC43','CHAdeMO','StandardType2')
			group by a2.address)a3
			on a1.address = a3.address 
''')

#put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
df_traffic = pd.read_sql_query(sql_traffic,conn)
df_ev_hv_cars = pd.read_sql_query(sql_registered_cars,conn)
df_charging_stations = pd.read_sql_query(sql_charging_station,conn)

fg= folium.FeatureGroup(name='Car traffic by road')
fgtwo = folium.FeatureGroup(name='Registered EV and HV')

def generateBaseMap(default_location=[53.547946, -7.716734], default_zoom_start=7):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

df_copy_traffic = df_traffic.copy()

df_day_list = []

for day in df_copy_traffic.day.sort_values().unique():
    df_day_list.append(df_copy_traffic.loc[df_copy_traffic.day == day, ['longitude', 'latitude', 'count']].groupby(['longitude', 'latitude']).sum().reset_index().values.tolist())

base_map = generateBaseMap()

HeatMap(data=df_copy_traffic[['longitude','latitude','vehiclecount']].groupby(['longitude','latitude']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(base_map)
HeatMapWithTime(df_day_list, radius=1, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(base_map)

for records in range(0,len(df_ev_hv_cars['county'])):
   folium.Circle(location=[df_ev_hv_cars.iloc[records][1],df_ev_hv_cars.iloc[records][2]],popup=[df_ev_hv_cars.iloc[records][0],df_ev_hv_cars.iloc[records][3]],radius=float(df_ev_hv_cars.iloc[records][3]),color='crimson',fill=True,fill_color='crimson').add_to(base_map)

for stations in range(0,len(df_charging_stations['address'])):
    folium.Circle(location=[df_charging_stations.iloc[stations][2],df_charging_stations.iloc[stations][1]],popup=df_charging_stations.iloc[stations][0],radius=1,color='#0080bb',fill=True,fill_color='#0080bb').add_to(base_map)

base_map.save("Traffic_by_road.html")