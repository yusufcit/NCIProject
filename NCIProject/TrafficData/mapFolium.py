import folium
import pandas
import json
import codecs


map = folium.Map(location=[39.908298, 32.846302], zoom_start=6,\
                      control_scale = True, tiles='Stamen Terrain')

fg= folium.FeatureGroup(name='My Map')


fg.add_child(folium.Marker(location=[38.750093, 30.556405],popup="AFYON <br> Adres: Marulcu Mah. Hacı Felahi Cad. Gökpınar Apt. No:31/1 AFYONKARAHİSAR <br>Telefon : +90 272 214 49 13 ", icon=folium.Icon(color='green')))
fg.add_child(folium.Marker(location=[40.679107, 35.834749],popup="AMASYA <br> Adres: Dere Kocacık Mah. Mustafa Kemal Cad. Ferit Yıldırım İş Hanı No:3 AMASYA <br> Telefon: +90 358 212 83 39", icon=folium.Icon(color='green')))

fg.add_child(folium.GeoJson(open("world_geojson_from_ogr.json",encoding = "utf-8-sig").read()))

map.add_child(fg)
map.save("Map2.html")