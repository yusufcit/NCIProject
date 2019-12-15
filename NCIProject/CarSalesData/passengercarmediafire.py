import os
import wget


from CarSalesData import pushtopsql


def carSales():
    currentDir = os.getcwd()
    print("The current working directory is %s" % currentDir)

    # define the name of the directory to be created
    location = "tmp/EVData/carsales"
    path = os.path.join(currentDir, location)
    print("full path is : %s" % os.path.join(currentDir, path))
    ### Creating Directory based on current location
    try:
        os.makedirs(path, 0o777)
    except OSError:
        print("Directory %s failed to create" % path)
    else:
        print("Directory %s created" % path)
    os.chdir(path)

    url = "http://download1500.mediafire.com/7u7w1juxqvlg/c1spuwklgzavig1/passengercars.csv"

    wget.download(url, path)

    ### Pushing to DB
    pushtopsql.insertIntoDB()



