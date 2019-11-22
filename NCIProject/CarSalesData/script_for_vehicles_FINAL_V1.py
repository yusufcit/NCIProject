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
import os #this library is used in order to remove the junk file once the loop is completed

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

time.sleep(1) #waits 1 second before clicking the filters

#Path for each block filters
date_path = driver.find_element_by_xpath("//*[contains(text(), 'Date')]") #date
registration_path = driver.find_element_by_xpath("//*[contains(text(), 'Registration Type')]") #registration type
vehicle_path = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[1]") #vehicle
geographic_path = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/a") #geographic

#Locate the filter, then open the filter
date_path.location_once_scrolled_into_view 
date_path.click()

registration_path.location_once_scrolled_into_view 
registration_path.click()

vehicle_path.location_once_scrolled_into_view
vehicle_path.click()

geographic_path.location_once_scrolled_into_view 
geographic_path.click()

#---------------------------------------------------/
#Static filter for comparaison date and for months /
#-------------------------------------------------/
    
time.sleep(1) #waits 1 second before clicking the filters
date_path.location_once_scrolled_into_view #locate the block filter for dates
driver.find_element_by_xpath("//select[@id='filter_comparison_year']/option[text()='2007']").click() #comparaison year. This is set to 2007 just in case in order to avoid any potential issues
driver.find_element_by_xpath("//select[@id='filter_date_month_from']/option[text()='January']").click() #filter from month - left as from JAN
driver.find_element_by_xpath("//select[@id='filter_date_month_to']/option[text()='December']").click() #filter to month - left as to DEC

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
        #Dimension: County
        #-----------------
        try:
            county = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/div[2]/div/div/div[2]/span/span").text #text for county taken from the filter box
            car_registration.append(county)
        except:
            car_registration.append("")       
        #Dimension: Car Make
        #-------------------
        try:
            car_make = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[4]/div/div[2]/div/div/table/tbody/tr/td[3]/span").text #static result as the loop should not affect it (we are only scraping one car at a time)
            car_registration.append(car_make)
        except:
            car_registration.append("")
        #Dimension: Model
        #----------------
        try:
            model = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[5]/div/div[2]/div/div/table/tbody/tr/td[4]/span").text #static result as the loop should not affect it (we are only scraping one car at a time)
            car_registration.append(model)
        except:
            car_registration.append("")   
        #Dimension: Registration type
        #----------------------------
        try:
            registration_type = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").text #This is coming from loop 2
            car_registration.append(registration_type)
        except:
            car_registration.append("")
        #Dimension: Age profile
        #----------------------
        if b==4:
            age_profile = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/span/span").text #This is coming from loop 2
            car_registration.append(age_profile) 
        else:
            car_registration.append('New')           
        #Dimension: Imported from
        #----------------------
        if b==4:
            imported_from = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/span/span").text #This is coming from loop 2
            car_registration.append(imported_from) 
        else:
            car_registration.append('New registrations')
        #Dimension: Transmission
        #-----------------------
        try:
            registration_type = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[10]/div/div[2]/div/div/table/tbody/tr/td[2]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
            car_registration.append(registration_type)
        except:
            car_registration.append("")
        #Dimension: Engine type
        #-----------------------
        try:
            engine_type = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[9]/div/div[2]/div/div/table/tbody/tr/td[2]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
            car_registration.append(engine_type)
        except:
            car_registration.append("")
        #Dimension: CO2 category
        #-----------------------
        #IMPORTANT: using a prius as an example, there are several bands. So the question is if we should take the worst band as a max? e.g. "<= 111-120"
        try:
            co2_category = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[6]/div/div[2]/div/div/table/tbody/tr/td[1]/span/div/div[1]").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
            car_registration.append(co2_category)
        except:
            car_registration.append("")
        #Dimension: CO2 band
        #-------------------
        #IMPORTANT: same as above
        try:
            co2_band = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[6]/div/div[2]/div/div/table/tbody/tr/td[1]/span/div/div[2]").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
            car_registration.append(co2_band)
        except:
            car_registration.append("")
        #Dimension: Segment
        #-------------------
        try:
            segment = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[7]/div/div[2]/div/div/table/tbody/tr/td[3]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
            car_registration.append(segment)
        except:
            car_registration.append("")
        #Dimension: Body type
        #--------------------
        try:
            body_type = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[8]/div/div[2]/div/div/table/tbody/tr/td[2]/span").text #Result based on filter. The loop should not affect it (we are only scraping one car at a time)
            car_registration.append(body_type)
        except:
            car_registration.append("")
        #Fact: Car registration count
        #-------------------------------
        try:
            car_registration_count = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[1]/td["+str(z)+"]/span").text
            car_registration.append(car_registration_count)
        except:
            car_registration.append("")
        #Add the records to the csv file
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if car_registration_count == '-' or car_registration_count == '0': #if there are no results, then there is no need to add the line in the csv (as no data. e.g.: You won't find a Tesla with a fuel engine)
            csvwriter_junk.writerow(car_registration) #if no results, then the records will be added to the junk file               
        else:
            csvwriter.writerow(car_registration) #adds the whole line created in the csv file

#===========================================================================================================

#PART IV: CREATE THE CSV FILE AND THE HEADER
#___________________________________________

#Variables created to simplify the data added to the csv file
#-------------------------------------------------------------

month = ['January','February','March','April','May','June','July','August','September','October','November','December']
passenger_cars_header = ['Year','Month','County','Car Make','Model','Registration type','Age profile','Imported from','Transmission','Engine type','CO2 category','CO2 band','Segment','Body type','Car registration count']

#Create a csv file
#-----------------
passenger_cars = open('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\passengercars.csv', 'w', newline='')
junk = open('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\junk.csv', 'w', newline='') #a junk file is created and will be deleted once the loop is completed

#Create the header for the csv file
#----------------------------------
csvwriter = csv.writer(passenger_cars)
csvwriter.writerow(passenger_cars_header)

csvwriter_junk = csv.writer(junk) #for the junk file

#===========================================================================================================

#PART V: LOOPS FOR FILTERS AND ADDS DATA TO THE CSV FILE
#_________________________________________________________

#Date filter
#-----------

years = []

#Loop 1: this is the loop the year filter
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
for a in range(1,14): #year loop (2019 to 2007)
    date_path.location_once_scrolled_into_view #locate the date block filter
    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/select/option["+str(a)+"]").click() #click on the year filter

    #Loop 2: this is the loop for geography (counties)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for c in range(1,31): #loop for counties (30 counties in total)
        if c==1 or c==7 or c==20 or c==27: #those are provinces and are subcategories that cannot be selected which will result in an error. So those are avoided
            continue
        else:
            time.sleep(1) #waits 1 seconds before opening the last filter
            geographic_path.location_once_scrolled_into_view #locate the geographic block filter
            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/div[2]/div/div").click() #opens the county options that can be selected 
            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/div[2]/div/div/ul/li["+str(c)+"]").click() #picks one county
            driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up

            #Loop 3: this is the loop for car brands/makes
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
            for d in range(1,91): #there are 90 different types of car brands
                time.sleep(1) #waits 1 seconds before opening the last filter
                vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div").click() #opens the car brand/make options that can be selected
                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div/ul/li["+str(d)+"]").click() #picks one brand
                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                
                #Loop 4: this is the loop for car body types
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                for e in range(1,55): #there are 54 different body types 
                    time.sleep(1) #waits 1 seconds before opening the last filter
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[3]/div").click() #opens the car body types options that can be selected
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[3]/div/ul/li["+str(e)+"]").click() #picks one body type
                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up

                    #Loop 5: this is the loop for car transmissions
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    for f in range(1,4): #there are 3 transmissions only
                        time.sleep(1) #waits 1 seconds before opening the last filter
                        vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                        driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div").click() #opens the car transmission options that can be selected
                        driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div/ul/li["+str(f)+"]").click() #picks one transmission
                        driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up

                        #Loop 6: this is the loop for car engine type
                        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        for g in range(1,15): #14 choices but choice 1 and 11 are subgroups that cannot be selected
                            if g==1 or g==11:
                                continue
                            else:
                                time.sleep(1) #waits 1 seconds before opening the last filter
                                vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div").click() #opens the engine type options that can be selected
                                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #picks one engine type
                                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                                
                                #Loop 7: this is the loop for car models
                                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
                                for h in range(2,102): #Different brand have different number of brands. So we will put a limit of 100 and put a try and except handler. Note that we start at 2 as the first option is a subcategory that cannot be selected 
                                    try:
                                        time.sleep(1) #waits 1 seconds before opening the last filter
                                        vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                                        driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div").click() #opens the car models options that can be selected
                                        driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/ul/li["+str(h)+"]").click() #picks one model
                                        driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                                    except:
                                        break  #when it breaks, that means that there are no more models to scrape! Happy days.
                                  
                                    #Loop 8: this is the loop for registration filter
                                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                    for b in range(1,5): #there are 4 registration types
                                        if b==1: #first option is omitted as it is the sum of new registration (option 2) and new import (option 3)
                                            continue
                                        elif b==4:
                                            time.sleep(2) #waits 2 seconds before opening the last filter
                                            registration_path.location_once_scrolled_into_view #locate the registration block filter
                                            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").click() #this is to select "Used Imports"
                                
                                            #Loop 8.1: Imported from if registration is "Used Imports"
                                            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                            for bb in range(1,5): #there are 4 different import categories
                                                registration_path.location_once_scrolled_into_view #locate the registration block filter
                                                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div").click() #opens the imported from options that can be selected 
                                                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/ul/li["+str(bb)+"]/span").click() #picks one of the option
                                                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                                            
                                                #Loop 8.2: Age profile if registration is "Age profile"
                                                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                for ba in range(1,12): #there are 11 age profiles
                                                    registration_path.location_once_scrolled_into_view #locate the registration block filter
                                                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div").click() #opens the age profile options that can be selected 
                                                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/ul/li["+str(ba)+"]/span").click() #picks one of the option
                                                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                                                    
                                                    #Apply the filters selected
                                                    #~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                    time.sleep(1) #waits 1 sec
                                                    driver.find_element_by_xpath("//*[contains(text(), 'Filter Results')]").click() #Once all the filters are setup, then this will close it and show the final results
                                                    time.sleep(1) # waits 1 second before proceeding to the next line of code
                                                    
                                                    #Create the records
                                                    #~~~~~~~~~~~~~~~~~~
                                                    create_record_for_csv()
                                                    
                                                    #Remove filter from loop 8.2: Age profile
                                                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
                                                    time.sleep(1) #waits 1 sec
                                                    registration_path.location_once_scrolled_into_view #locate the registration block filter
                                                    time.sleep(1) #waits 1 sec
                                                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div").click() #opens the age profile options that can be selected                     
                                                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/span/i").click() #unselect the age profile choice in filter 
                                                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                                        
                                                #Remove the filter from loop 8.1: Used imports
                                                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
                                                time.sleep(1) #waits 1 sec
                                                registration_path.location_once_scrolled_into_view #locate the registration block filter
                                                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div").click() #opens the import from options that can be selected                     
                                                time.sleep(1) #waits 1 sec
                                                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/span/i").click() #unselect the choice in imported from filter 
                                                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                                        
                                        else:
                                            time.sleep(1) #waits 1 second before opening the last filter
                                            registration_path.location_once_scrolled_into_view #locate the registration block filter
                                            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").click() #picks the other age profile options
                                
                                            #Apply the filters selected
                                            #~~~~~~~~~~~~~~~~~~~~~~~~~~
                                            driver.find_element_by_xpath("//*[contains(text(), 'Filter Results')]").click() #Once all the filters are setup, then this will close it and show the final results
                                            time.sleep(1) # waits 1 second before proceeding to the next line of code
                                        
                                            #Create the records
                                            #~~~~~~~~~~~~~~~~~~
                                            #the below paste the final output in the csv file
                                            create_record_for_csv()
                        
                                    #Remove the filter from loop 7: car models
                                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                    time.sleep(1) #waits 1 sec
                                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/span/i").click() #unselect the car model in filter
                                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up

                                #Remove the filter from loop 6: engine type
                                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                time.sleep(1) #waits 1 sec
                                vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/div[2]/span/i").click() #unselect the engine type in filter
                                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up

                        #Remove the filter from loop 5: car transmissions
                        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        time.sleep(1) #waits 1 sec
                        vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                        driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[4]/div/div[2]/span/i").click() #unselect the car transmission in filter
                            
                    #Remove the filter from loop 4: car body types
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    time.sleep(1) #waits 1 sec
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[3]/div/div[2]/span/i").click() #unselect the body type in filter
                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
   
                #Remove the filter from loop 3: car brand/makes
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                time.sleep(1) #waits 1 sec
                vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/span/i").click() #unselect the car brand in filter
                driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
                                
            #Remove filter from loop 2: geography
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
            time.sleep(1) #waits 1 sec
            geographic_path.location_once_scrolled_into_view #locate the geographic block filter
            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/div[2]/div/div/div[2]/span/i").click() #unselect the county in filter
            driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up

#===========================================================================================================

#PART VI: CLOSE THE CSV FILE
#___________________________
        
passenger_cars.close()

#===========================================================================================================

#PART VII: CONFIRM THAT THE SCRAPING IS COMPLETE
#______________________________________________
        
print('SCRAPPING IS NOW SUCCESSFULLY COMPLETE!!!')

#===========================================================================================================

#PART VIII: CLOSE AND DELETE THE JUNK FILE
#_________________________________________

junk.close() #closes the junk file
os.remove('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\junk.csv') #delete the junk file