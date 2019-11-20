import datetime


class GetDownloadLinks:
    def __init__(self, fromDate, toDate):
        self.fromDate = fromDate
        self.toDate = toDate


def geturls(fromDate, toDate):
    duration = toDate - fromDate
    print(duration.days)
    urls = []
    for i in range(duration.days):
        fromDate += datetime.timedelta(days=1)
        url = "https://data.tii.ie/Datasets/TrafficCountData/" + fromDate.strftime(
            "%Y/%m/%d") + "/per-site-class-aggr-" + fromDate.strftime("%Y-%m-%d") + ".csv"
        urls.append(url)
        # print(urls[i])
        # print(i)
    return urls
