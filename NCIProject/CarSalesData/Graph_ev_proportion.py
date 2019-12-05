#https://jakevdp.github.io/PythonDataScienceHandbook/04.02-simple-scatter-plots.html
#https://stackoverflow.com/questions/18458734/python-plot-list-of-tuples
#https://www.dataquest.io/blog/python-pandas-databases/

import psycopg2
import pandas as pd
import plotly.express as px #https://plot.ly/python/templates/

#https://plot.ly/python/hover-text-and-formatting/
#https://plot.ly/python/line-and-scatter/
#import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

#the below is to log into our database
conn = psycopg2.connect("host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

#SQL query
sql = ('''select distinct 
a1.county, 
a1.year, 
a3.EV_and_HV, 
a5.total_cars_registered,  
round(cast(a3.EV_and_HV as decimal)/cast(a5.total_cars_registered as decimal)*100,2) as EV_HV_PROPORTION

from registrations a1 

left join (select 
			a2.county, 
			a2.year, 
			sum(a2.carregistrationcount) as EV_and_HV  

			from public.registrations a2
		  	where a2.enginetype in ('Electric','Hybrid')
			group by
			a2.county, 
			a2.year  
			) a3 on a1.county = a3.county and a1.year = a3.year

left join (select 
		   a4.county,
		   a4.year,
		   sum(a4.carregistrationcount) as total_cars_registered
			from public.registrations a4
			group by 
		   a4.county,
		   a4.year	
		   )a5 on a1.county = a5.county and a1.year = a5.year
		   
order by a1.county asc, a1.year desc''')

#put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
df = pd.read_sql_query(sql,conn)

fig = px.scatter(df,x="total_cars_registered",y="ev_and_hv",color="county",size="ev_hv_proportion",hover_data=["year"])
fig.show()
