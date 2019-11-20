#OOOOOOOOOOOOOOOOOOOOOOOO
#O Project: EV VEHICLES O
#OOOOOOOOOOOOOOOOOOOOOOOO

#PART I: USE OF SELENIUM TO ACCESS THE WEBSITE
#_____________________________________________

#----------/
#Libraries/
#--------/

from selenium import webdriver #this is used so that we can click on the website
import csv #this is used in order to create a csv file
import time #this is used in order to pause in sec wherever needed before the next line of code runs

#-----------------/
#Open the website/
#---------------/

driver = webdriver.Chrome('C:\\Users\\alain\\Documents\\chromedriver.exe')
site = driver.get('https://stats.beepbeep.ie/')  # go to web-page

#===========================================================================================================

#PART II: PREPARE THE FILTERS
#____________________________

#-----------------/
#Open all filter /
#---------------/

time.sleep(5) #waits 5 seconds before opening the filters
driver.find_element_by_xpath("//*[contains(text(), 'Date')]").click()
driver.find_element_by_xpath("//*[contains(text(), 'Registration Type')]").click()
driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[1]").click() #vehicle filter
time.sleep(2) #waits 2 seconds before opening the last filter
try:
    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/a").click() #geographic filter
except:
    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/a").click() #for some reasons, this has to be clicked twice before it appears

#---------------------------------------------------/
#Static filter for comparaison date and for months /
#-------------------------------------------------/
    
time.sleep(15) #waits 15 seconds before clicking the filters
driver.find_element_by_xpath("//select[@id='filter_comparison_year']/option[text()='2007']").click() #comparaison year. This is set to 2007 just in case in order to avoid any potential issues
#IMPORTANT: ALWAYS LEAVE THIS FILTER AS JANUARY. FOR OUR PURPOSE, THERE IS NO NEED TO LOOP THIS!!!
driver.find_element_by_xpath("//select[@id='filter_date_month_from']/option[text()='January']").click() #filter from month
#IMPORTANT: ALWAYS LEAVE THIS FILTER AS DECEMBER. FOR OUR PURPOSE, THERE IS NO NEED TO LOOP THIS!!!
driver.find_element_by_xpath("//select[@id='filter_date_month_to']/option[text()='December']").click() #filter to month

#===========================================================================================================

#PART III: CREATE FUNCTIONS
#__________________________

def create_record_for_csv():
    '''Create the records
    the below looks for the data, copy it and paste it in the car_registration variable before being added as a row in the csv file'''
    for z in range(2,14): #there are 12 months and the first data for Jan starts where b=2
        car_registration = []
        #Dimension: Year
        #----------------
        year = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[1]/td["+str(1)+"]/span").text #Note that this is static (str(1)) as we are always picking the year that we filtered
        car_registration.append(year)
        #Dimension: Month
        #----------------
        car_registration.append(month[z-2]) #this is pulling the month from the variable created in II/
        #Dimension: Car Make
        #-------------------
        car_make = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[4]/div/div[2]/div/div/table/tbody/tr/td[3]/span").text #static result as the loop should not affect it (we are only scraping one car at a time)
        car_registration.append(car_make)
        #Dimension: Model
        #----------------
        model = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[5]/div/div[2]/div/div/table/tbody/tr/td[4]/span").text #static result as the loop should not affect it (we are only scraping one car at a time)
        car_registration.append(model)
        #Dimension: Registration type
        #----------------------------
        registration_type = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").text #This is coming from loop 2
        car_registration.append(registration_type)
        #Dimension: Age profile
        #----------------------
        if b==4:
            age_profile = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/span/span").text #This is coming from loop 2
            car_registration.append(age_profile) 
        else:
            car_registration.append('New')
        #Dimension: Transmission
        #-----------------------
        registration_type = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[10]/div/div[2]/div/div/table/tbody/tr/td[2]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
        car_registration.append(registration_type)
        #Dimension: Engine type
        #-----------------------
        engine_type = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[9]/div/div[2]/div/div/table/tbody/tr/td[2]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
        car_registration.append(engine_type)
        #Dimension: CO2 category
        #-----------------------
        #IMPORTANT: using a prius as an example, there are several bands. So the question is if we should take the worst band as a max? e.g. "<= 111-120"
        co2_category = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[6]/div/div[2]/div/div/table/tbody/tr/td[1]/span/div/div[1]").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
        car_registration.append(co2_category)
        #Dimension: CO2 band
        #-------------------
        #IMPORTANT: same as above
        co2_band = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[6]/div/div[2]/div/div/table/tbody/tr/td[1]/span/div/div[2]").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
        car_registration.append(co2_band)
        #Dimension: Segment
        #-------------------
        segment = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[7]/div/div[2]/div/div/table/tbody/tr/td[3]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
        car_registration.append(segment)
        #Dimension: Body type
        #--------------------
        body_type = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[8]/div/div[2]/div/div/table/tbody/tr/td[2]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
        car_registration.append(body_type)
        #Fact: Car registration count
        #-------------------------------
        car_registration_count = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[1]/td["+str(z)+"]/span").text
        car_registration.append(car_registration_count)
        
        #Add the records to the csv file
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if car_registration_count == '-': #if there are no results, then there is no need to add the line in the csv (as no data. e.g.: You won't find a Tesla with a fuel engine)
            continue                 
        else:
            csvwriter.writerow(car_registration) #adds the whole line created in the csv file



#===========================================================================================================

#PART IV: CREATE THE CSV FILE AND THE HEADER
#___________________________________________

#Variables created to simplify the data added to the csv file
#-------------------------------------------------------------

month = ['January','February','March','April','May','June','July','August','September','October','November','December']
passenger_cars_header = ['Year','Month','Car Make','Model','Registration type','Age profile','Transmission','Engine type','CO2 category','CO2 band','Segment','Body type','Car registration count']

#Create a csv file
#-----------------
passenger_cars = open('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\passengercars.csv', 'w', newline='')

#Create the header for the csv file
#----------------------------------
csvwriter = csv.writer(passenger_cars)
csvwriter.writerow(passenger_cars_header)

#===========================================================================================================

#PART V: LOOPS FOR FILTERS AND ADDS DATA TO THE CSV FILE
#_________________________________________________________

#Date filter
#-----------

years = []

#Loop 1: this is the loop the year filter
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
for a in range(1,14): 
    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/select/option["+str(a)+"]").click()

    #Loop 2: this is the loop for registration filter
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for b in range(1,5): 
        if b==1:
            continue
        elif b==4:
            time.sleep(2) #waits 2 seconds before opening the last filter
            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").click() #this is to select "Used Imports"
            
            #Loop 2.1: Age profile if registration is "Used Imports"
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            for ba in range(1,12): #there are 11 age profiles
                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div").click() #opens the age profile options that can be selected 
                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/ul/li["+str(ba)+"]/span").click() #picks one of the option
                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                
                #Apply the filters selected
                #~~~~~~~~~~~~~~~~~~~~~~~~~~
                time.sleep(2) #waits 2 sec
                driver.find_element_by_xpath("//*[contains(text(), 'Filter Results')]").click() #Once all the filters are setup, then this will close it and show the final results
                time.sleep(1) # waits X seconds before proceeding to the next line of code
                
                #Create the records
                #~~~~~~~~~~~~~~~~~~
                create_record_for_csv()
                
                #Remove the filter from loop 2.1
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div").click() #opens the age profile options that can be selected                     
                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/span/i").click() #unselect the choice in filter 
                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
        
        else:
            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").click() #picks the other age profile options

            #Apply the filters selected
            #~~~~~~~~~~~~~~~~~~~~~~~~~~
            driver.find_element_by_xpath("//*[contains(text(), 'Filter Results')]").click() #Once all the filters are setup, then this will close it and show the final results
            time.sleep(1) # waits X seconds before proceeding to the next line of code
        
            #Create the records
            #~~~~~~~~~~~~~~~~~~
            #the below looks for the data, copy it and paste it in the car_registration variable before being added as a row in the csv file
            create_record_for_csv()

#===========================================================================================================

#PART VI: CLOSE THE CSV FILE
#___________________________
        
passenger_cars.close()

#===========================================================================================================

#PART VII: CONFIRM THAT THE SCRAPING IS COMPLETE
#______________________________________________
        
print('SCRAPPING IS NOW SUCCESSFULLY COMPLETE!!!')

#===========================================================================================================
#Once completed clear the filters
#--------------------------------
driver.find_element_by_xpath("//*[contains(text(), 'Clear Filters')]").click() 



















 













