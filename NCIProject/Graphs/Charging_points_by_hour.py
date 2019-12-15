#https://medium.com/@pknerd/data-visualization-in-python-line-graph-in-matplotlib-9dfd0016d180
#https://stackoverflow.com/questions/28337117/how-to-pivot-a-dataframe-in-pandas
#https://plot.ly/python/text-and-annotations/
import os
import psycopg2
import pandas as pd


def ChargingPointByHour():
    try:
        # the below is to log into our database
        conn = psycopg2.connect(
            "host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

        # SQL query
        sql = ('''select 
            CASE 
            when UPPER(a1.address) like ('%CARLOW%') then 'CARLOW'
            when UPPER(a1.address) like ('%CAVAN%') then 'CAVAN'
            when UPPER(a1.address) like ('%CLARE%') then 'CLARE'
            when UPPER(a1.address) like ('%CORK%') then 'CORK'
            when UPPER(a1.address) like ('%DONEGAL%') then 'DONEGAL'
            when UPPER(a1.address) like ('%DUBLIN%') then 'DUBLIN'
            when UPPER(a1.address) like ('%GALWAY%') then 'GALWAY'
            when UPPER(a1.address) like ('%KERRY%') then 'KERRY'
            when UPPER(a1.address) like ('%KILDARE%') then 'KILDARE'
            when UPPER(a1.address) like ('%KILKENNY%') then 'KILKENNY'
            when UPPER(a1.address) like ('%LAOIS%') then 'LAOIS'
            when UPPER(a1.address) like ('%LEITRIM%') then 'LEITRIM'
            when UPPER(a1.address) like ('%LIMERICK%') then 'LIMERICK'
            when UPPER(a1.address) like ('%LONGFORD%') then 'LONGFORD'
            when UPPER(a1.address) like ('%LOUTH%') then 'LOUTH'
            when UPPER(a1.address) like ('%MAYO%') then 'MAYO'
            when UPPER(a1.address) like ('%MEATH%') then 'MEATH'
            when UPPER(a1.address) like ('%MONAGHAN%') then 'MONAGHAN'
            when UPPER(a1.address) like ('%OFFALY%') then 'OFFALY'
            when UPPER(a1.address) like ('%ROSCOMMON%') then 'ROSCOMMON'
            when UPPER(a1.address) like ('%SLIGO%') then 'SLIGO'
            when UPPER(a1.address) like ('%TIPPERARY%') then 'TIPPERARY'
            when UPPER(a1.address) like ('%WATERFORD%') then 'WATERFORD'
            when UPPER(a1.address) like ('%WESTMEATH%') then 'WESTMEATH'
            when UPPER(a1.address) like ('%WEXFORD%') then 'WEXFORD'
            when UPPER(a1.address) like ('%WICKLOW%') then 'WICKLOW'
            else 'OTHERS'
            END as COUNTY, 

            left(a1.daytime,2) as hour, 

            round(sum(CASE a1.status
            when 'Part' then 0.5
            when 'Occ' then 1
            else 0
            END)/ count(a1.status),2) as average_charging_usage  

            from public.evchargetext a1 

            where a1.chargepointtype in ('ComboCCS','CHAdeMO','StandardType2','FastAC43')
            and  left(a1.recorddate,4) like ('2019%')

            group by 1,2 ''')

        # put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
        df = pd.read_sql_query(sql, conn)

        output = pd.pivot_table(df, values='average_charging_usage', index='hour', columns='county').reset_index()

        ax = output.plot(title='Average usage of charging points per county and per hour', rot=30, colormap='jet')
        # ax = output.plot(xticks=output.index)
        ylab = ax.set_ylabel('Usage ratio from 0% to 100%')
        lg = ax.legend(ncol=4, loc=2, bbox_to_anchor=(1.05, 1))

        # Save as .png
        if not os.path.exists("graphImages"):
            os.mkdir("graphImages")
        fig = ax.get_figure()
        fig.savefig("graphImages/Appendix6_ChargingPointsByHour.png", dpi=100)
    except:
        print("Failed to get Charging point graph by hour")

