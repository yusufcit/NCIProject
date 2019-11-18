import datetime

## This will give the urls to download traffic data
date = datetime.date(2019,11,1)
currentDate = datetime.datetime.now().date()
difference = currentDate - date
print(difference.days)
for i in range(difference.days):
    date += datetime.timedelta(days=1)
    strDate = date.strftime("%Y-%m-%d")
    url = "https://data.tii.ie/Datasets/TrafficCountData/"+ date.strftime("%Y/%m/%d") +"/per-site-class-aggr-"+ date.strftime("%Y-%m-%d") +".csv"
    print(url)



