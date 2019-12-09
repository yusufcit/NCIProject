from ChargingPointData import EVChargingPoint
from TrafficData import getTrafficDataSoup


class EntryPoint:
    def main():
        getTrafficDataSoup.gatherTrafficData()
        EVChargingPoint.getChargingPointData()
    if __name__ == "__main__":
        main()
