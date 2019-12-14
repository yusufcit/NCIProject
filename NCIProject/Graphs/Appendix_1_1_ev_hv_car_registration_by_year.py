import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#the below is to log into our database
conn = psycopg2.connect("host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

#SQL query
sql = ('''select 
a1.year, 
sum(a1.carregistrationcount) as ev_hv_registered_cars_count
from public.registrations a1
where a1.enginetype in ('Electric','Hybrid')
group by 1
order by a1.year asc ''')

#put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
df = pd.read_sql_query(sql,conn)

# Number of bars to be created
y_pos = np.arange(len(df['year']))

# Create bars
plt.bar(y_pos, df['ev_hv_registered_cars_count'])

# Create names on the x-axis
plt.xticks(y_pos,df['year'])

#Add axis
plt.title('Electric and hybrid car registrations count by year')
plt.ylabel('ev and hv car counts')
plt.xlabel('Year')

# Show graphic
plt.show()