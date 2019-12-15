from CarSalesData import passengercarmediafire
from ChargingPointData import EVChargingPoint
from Graphs import Ev_hv_car_registration_by_year, Charging_points_count_by_year, \
    Vehiclecount_per_road, Ev_proportion, ChargingPointsCorrelation, \
    Ev_per_charging_point, Charging_points_by_hour
from TrafficData import getTrafficDataSoup


def main():
    getTrafficDataSoup.gatherTrafficData()
    EVChargingPoint.getChargingPointData()
    passengercarmediafire.carSales()
    Ev_hv_car_registration_by_year.carRegByYear()
    Charging_points_count_by_year.ChargingPointCountByYear()
    Vehiclecount_per_road.VehicaleCountPerRoad()
    Ev_proportion.evProportion()
    ChargingPointsCorrelation.chargPointCorrolation()
    Ev_per_charging_point.evPerCharingPoint()
    Charging_points_by_hour.ChargingPointByHour()

    print("yaeeeea !!!! its Finished......")
    print("All the visualization files are saved in 'graphImages' Directory in the project")

if __name__ == "__main__":
    main()
