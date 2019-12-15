#https://medium.com/dunder-data/selecting-subsets-of-data-in-pandas-6fcd0170be9c
import os

import psycopg2
import pandas as pd
import plotly.graph_objects as go



def evPerCharingPoint():
    try:
        # the below is to log into our database
        conn = psycopg2.connect(
            "host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

        # SQL query
        sql = ('''select 
        UPPER(b1.county) as County, 
        sum(b1.carregistrationcount) as EV_HV_count, 
        a3.chargin_point_counts, 
        sum(b1.carregistrationcount)/a3.chargin_point_counts as EV_HV_PER_CHARGING_POINT

        from public.registrations b1

        left join (select
        			CASE 
        			when UPPER(a2.address) like ('%CARLOW%') then 'CARLOW'
        			when UPPER(a2.address) like ('%CAVAN%') then 'CAVAN'
        			when UPPER(a2.address) like ('%CLARE%') then 'CLARE'
        			when UPPER(a2.address) like ('%CORK%') then 'CORK'
        			when UPPER(a2.address) like ('%DONEGAL%') then 'DONEGAL'
        			when UPPER(a2.address) like ('%DUBLIN%') then 'DUBLIN'
        			when UPPER(a2.address) like ('%GALWAY%') then 'GALWAY'
        			when UPPER(a2.address) like ('%KERRY%') then 'KERRY'
        			when UPPER(a2.address) like ('%KILDARE%') then 'KILDARE'
        			when UPPER(a2.address) like ('%KILKENNY%') then 'KILKENNY'
        			when UPPER(a2.address) like ('%LAOIS%') then 'LAOIS'
        			when UPPER(a2.address) like ('%LEITRIM%') then 'LEITRIM'
        			when UPPER(a2.address) like ('%LIMERICK%') then 'LIMERICK'
        			when UPPER(a2.address) like ('%LONGFORD%') then 'LONGFORD'
        			when UPPER(a2.address) like ('%LOUTH%') then 'LOUTH'
        			when UPPER(a2.address) like ('%MAYO%') then 'MAYO'
        			when UPPER(a2.address) like ('%MEATH%') then 'MEATH'
        			when UPPER(a2.address) like ('%MONAGHAN%') then 'MONAGHAN'
        			when UPPER(a2.address) like ('%OFFALY%') then 'OFFALY'
        			when UPPER(a2.address) like ('%ROSCOMMON%') then 'ROSCOMMON'
        			when UPPER(a2.address) like ('%SLIGO%') then 'SLIGO'
        			when UPPER(a2.address) like ('%TIPPERARY%') then 'TIPPERARY'
        			when UPPER(a2.address) like ('%WATERFORD%') then 'WATERFORD'
        			when UPPER(a2.address) like ('%WESTMEATH%') then 'WESTMEATH'
        			when UPPER(a2.address) like ('%WEXFORD%') then 'WEXFORD'
        			when UPPER(a2.address) like ('%WICKLOW%') then 'WICKLOW'
        			else 'OTHERS'
        			END as COUNTY, 

        			count(a2.address) as chargin_point_counts

        			from (SELECT distinct 
        					a1.address, 
        					max(a1.recorddate),
        					max(a1.daytime) 
        					FROM public.evchargetext a1
        					where a1.chargepointtype in ('ComboCCS','FastAC43','CHAdeMO','StandardType2')
        					group by a1.address)a2

        			group by 
        			CASE 
        			when UPPER(a2.address) like ('%CARLOW%') then 'CARLOW'
        			when UPPER(a2.address) like ('%CAVAN%') then 'CAVAN'
        			when UPPER(a2.address) like ('%CLARE%') then 'CLARE'
        			when UPPER(a2.address) like ('%CORK%') then 'CORK'
        			when UPPER(a2.address) like ('%DONEGAL%') then 'DONEGAL'
        			when UPPER(a2.address) like ('%DUBLIN%') then 'DUBLIN'
        			when UPPER(a2.address) like ('%GALWAY%') then 'GALWAY'
        			when UPPER(a2.address) like ('%KERRY%') then 'KERRY'
        			when UPPER(a2.address) like ('%KILDARE%') then 'KILDARE'
        			when UPPER(a2.address) like ('%KILKENNY%') then 'KILKENNY'
        			when UPPER(a2.address) like ('%LAOIS%') then 'LAOIS'
        			when UPPER(a2.address) like ('%LEITRIM%') then 'LEITRIM'
        			when UPPER(a2.address) like ('%LIMERICK%') then 'LIMERICK'
        			when UPPER(a2.address) like ('%LONGFORD%') then 'LONGFORD'
        			when UPPER(a2.address) like ('%LOUTH%') then 'LOUTH'
        			when UPPER(a2.address) like ('%MAYO%') then 'MAYO'
        			when UPPER(a2.address) like ('%MEATH%') then 'MEATH'
        			when UPPER(a2.address) like ('%MONAGHAN%') then 'MONAGHAN'
        			when UPPER(a2.address) like ('%OFFALY%') then 'OFFALY'
        			when UPPER(a2.address) like ('%ROSCOMMON%') then 'ROSCOMMON'
        			when UPPER(a2.address) like ('%SLIGO%') then 'SLIGO'
        			when UPPER(a2.address) like ('%TIPPERARY%') then 'TIPPERARY'
        			when UPPER(a2.address) like ('%WATERFORD%') then 'WATERFORD'
        			when UPPER(a2.address) like ('%WESTMEATH%') then 'WESTMEATH'
        			when UPPER(a2.address) like ('%WEXFORD%') then 'WEXFORD'
        			when UPPER(a2.address) like ('%WICKLOW%') then 'WICKLOW'
        			else 'OTHERS'
        			END  
        		  ) a3
        		  on a3.COUNTY = UPPER(b1.county)

        where b1.enginetype in ('Electric','Hybrid')
        and UPPER(b1.county) not in ('WESTMEATH') --There is not charging station in Westmeath

        group by 
        UPPER(b1.county), 
        a3.chargin_point_counts

        order by sum(b1.carregistrationcount)/a3.chargin_point_counts desc''')

        # put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
        df = pd.read_sql_query(sql, conn)

        colors = ['lightslategray', ] * 20
        colors[0] = 'crimson'

        # pick the figure and the data
        fig = go.Figure(data=[go.Bar(x=df['county'], y=df['ev_hv_per_charging_point'], marker_color=colors)])

        # add title to graph
        fig.update_layout(title_text='Electric and hybrid vehicle per charging point by county')

        # save as .png
        if not os.path.exists("graphImages"):
            os.mkdir("graphImages")
        fig.write_image("graphImages/Appendix5_EvPerChargingPoint.png")
    except:
        print("Failed to get EV per charging point")