import folium as folium

for lat, lon, traffic_q, traffic, bike, city in zip(df['latitude'], df['longitude'], df['traffic_index_quartile'], df['traffic_index'], df['bike_score'], df['city']):
    folium.CircleMarker(
        [lat, lon],
        radius=.15*bike,
        popup = ('City: ' + str(city).capitalize() + '<br>'
                 'Bike score: ' + str(bike) + '<br>'
                 'Traffic level: ' + str(traffic) +'%'
                ),
        color='b',
        key_on = traffic_q,
        threshold_scale=[0,1,2,3],
        fill_color=colordict[traffic_q],
        fill=True,
        fill_opacity=0.7
        ).add_to(traffic_map)
traffic_map