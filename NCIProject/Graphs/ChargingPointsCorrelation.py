#https://machinelearningmastery.com/how-to-use-correlation-to-understand-the-relationship-between-variables/
import os

import psycopg2
import pandas as pd
# generate related variables
from numpy import mean
from numpy import std
from matplotlib import pyplot
#correlation analysis
from scipy.stats import pearsonr
from scipy.stats import spearmanr


def chargPointCorrolation():
    try:
        # the below is to log into our database
        conn = psycopg2.connect(
            "host=nciproject.postgres.database.azure.com dbname=ev_ireland user=nciadmin@nciproject password=Nciproject01?")

        # SQL query
        sql = ('''select 

            b1.COUNTY, 
            b1.year, 
            b1.month, 
            b1.day,
            b1.average_charging_usage, 
            b2.traffic_count

            -----------------------THIS IS THE SQL FOR CHARGING POINTS-----------------------
            from 
            		(select 
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

            		left(a1.recorddate,4) as year, 
            		right(left(a1.recorddate,6),2) as month, 
            		right(a1.recorddate,2) as day, 

            		round(sum(CASE a1.status
            		when 'Part' then 0.5
            		when 'Occ' then 1
            		else 0
            		END)/ count(a1.status),2) as average_charging_usage  

            		from public.evchargetext a1 

            		where a1.chargepointtype in ('ComboCCS','CHAdeMO','StandardType2','FastAC43')
            		and  left(a1.recorddate,4) like ('%2018%')

            		group by 1,2,3,4) b1

            -----------------------THIS IS THE SQL FOR TRAFFIC DATA-----------------------
            inner join 
            		(select 
            		CASE 
            		when UPPER(a2.description) like ('%CARLOW%') then 'CARLOW'
            		when UPPER(a2.description) like ('%CAVAN%') then 'CAVAN'
            		when UPPER(a2.description) like ('%CLARE%') then 'CLARE'
            		when UPPER(a2.description) like ('%CORK%') then 'CORK'
            		when UPPER(a2.description) like ('%DONEGAL%') then 'DONEGAL'
            		when UPPER(a2.description) like ('%DUBLIN%') then 'DUBLIN'
            		when UPPER(a2.description) like ('%GALWAY%') then 'GALWAY'
            		when UPPER(a2.description) like ('%KERRY%') then 'KERRY'
            		when UPPER(a2.description) like ('%KILDARE%') then 'KILDARE'
            		when UPPER(a2.description) like ('%KILKENNY%') then 'KILKENNY'
            		when UPPER(a2.description) like ('%LAOIS%') then 'LAOIS'
            		when UPPER(a2.description) like ('%LEITRIM%') then 'LEITRIM'
            		when UPPER(a2.description) like ('%LIMERICK%') then 'LIMERICK'
            		when UPPER(a2.description) like ('%LONGFORD%') then 'LONGFORD'
            		when UPPER(a2.description) like ('%LOUTH%') then 'LOUTH'
            		when UPPER(a2.description) like ('%MAYO%') then 'MAYO'
            		when UPPER(a2.description) like ('%MEATH%') then 'MEATH'
            		when UPPER(a2.description) like ('%MONAGHAN%') then 'MONAGHAN'
            		when UPPER(a2.description) like ('%OFFALY%') then 'OFFALY'
            		when UPPER(a2.description) like ('%ROSCOMMON%') then 'ROSCOMMON'
            		when UPPER(a2.description) like ('%SLIGO%') then 'SLIGO'
            		when UPPER(a2.description) like ('%TIPPERARY%') then 'TIPPERARY'
            		when UPPER(a2.description) like ('%WATERFORD%') then 'WATERFORD'
            		when UPPER(a2.description) like ('%WESTMEATH%') then 'WESTMEATH'
            		when UPPER(a2.description) like ('%WEXFORD%') then 'WEXFORD'
            		when UPPER(a2.description) like ('%WICKLOW%') then 'WICKLOW'
            		else 'OTHERS'
            		END as COUNTY, 

            		a2.year, 
            		a2.month, 
            		a2.day, 
            		sum(a2.vehiclecount) as traffic_count 

            		from public.trafficdata a2 

            		where a2.year = 2018

            		group by 1,2,3,4) b2
            		on b2.COUNTY = b1.COUNTY 
            		and cast(b2.year as integer) = cast(b1.year as integer) 
            		and cast(b2.month as integer) = cast(b1.month as integer) 
            		and cast(b2.day as integer) = cast(b1.day as integer)

            where b1.COUNTY not in ('OTHERS')''')

        # put the results in a nice table which will make it easy to manipulate. Otherwise, the data are saved in a list of tuples that are harder to manipulate.
        df = pd.read_sql_query(sql, conn)

        # fig = px.scatter(df,x="total_cars_registered",y="ev_and_hv",color="county",size="ev_hv_proportion",hover_data=["year"])
        # fig.show()

        # summarize
        print('Charging_coefficient: mean=%.3f stdv=%.3f' % (
            mean(df['average_charging_usage']), std(df['average_charging_usage'])))
        print('Traffic: mean=%.3f stdv=%.3f' % (mean(df['traffic_count']), std(df['traffic_count'])))
        # plot
        pyplot.scatter(df['average_charging_usage'], df['traffic_count'])
        pyplot.suptitle('Correlation between charging occupancy rate and traffic by county', fontsize=20)
        pyplot.xlabel('Average charging occupancy rate (From 0 to 1)', fontsize=18)
        pyplot.ylabel('Total traffic per county', fontsize=16)

        pyplot.show()
        # saving image of the figure
        if not os.path.exists("graphImages"):
            os.mkdir("graphImages")
        pyplot.savefig("graphImages/ChargingPointsCorrelation.png")

        # calculate Pearson's correlation
        corr, _ = pearsonr(df['average_charging_usage'], df['traffic_count'])
        print('Pearsons correlation: %.3f' % corr)

        # calculate spearman's correlation
        corr, _ = spearmanr(df['average_charging_usage'], df['traffic_count'])
        print('Spearmans correlation: %.3f' % corr)
        conn.close()
    except:
        print("Failed to get traffic and charging point correlation")



