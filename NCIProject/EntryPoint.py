from TrafficData import getTrafficDataSoup


class EntryPoint:
    def main():
        getTrafficDataSoup.gatherTrafficData()

    if __name__ == "__main__":
        main()
