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
        #1 Dimension: Year
        #-----------------
        year = driver.find_element_by_xpath("//div/div[3]/div/div[2]/div[3]/div/div[2]/div/div/table/tbody/tr[1]/td["+str(1)+"]/span").text #Note that this is static (str(1)) as we are always picking the year that we filtered
        car_registration.append(year)
        #2 Dimension: Month
        #------------------
        car_registration.append(month[z-2]) #this is pulling the month from the variable created in II/
        #3 Dimension: County
        #-------------------
        try:
            county = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[4]/div[2]/div/div/div[2]/span/span").text #text for county taken from the filter box
            car_registration.append(county)
        except:
            car_registration.append("")       
        #4 Dimension: Registration type
        #------------------------------
        try:
            registration_type = driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").text 
            car_registration.append(registration_type)
        except:
            car_registration.append("")
        #5 Dimension: Engine type 
        #-------------------------
        try:
            if g==2:
                car_registration.append('Non electric')
            elif g==4:
                car_registration.append('Electric')
            else:
                car_registration.append('Hybrid')      
        except:
            car_registration.append("")
        #6 Fact: Car registration count
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
#passenger_cars_header = ['Year','Month','County','Car Make','Model','Registration type','Age profile','Imported from','Transmission','Engine type','CO2 category','CO2 band','Segment','Body type','Car registration count']
passenger_cars_header = ['Year','Month','County','Registration type','Engine type','Car registration count']

#Create a csv file
#-----------------
passenger_cars = open('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\passengercars_summary.csv', 'w', newline='')
junk = open('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\junk_summary.csv', 'w', newline='') #a junk file is created and will be deleted once the loop is completed

#Create the header for the csv file
#----------------------------------
csvwriter = csv.writer(passenger_cars)
csvwriter.writerow(passenger_cars_header)

csvwriter_junk = csv.writer(junk) #for the junk file

#===========================================================================================================

#PART V: LOOPS FOR FILTERS AND ADDS DATA TO THE CSV FILE
#_________________________________________________________

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

#********1               
            #Loop 3: this is the loop for car engine type
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            for g in range(1,13):
                if g==1 or g==3 or g==5 or g==6 or g==7 or g==8 or g==9 or g==10 or g==11: #these will be grouped. g=11 is a subgroup
                    continue
                elif g==2: #non electric
                    time.sleep(1)
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div").click() #opens the engine type options that can be selected
                          
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #diesel
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #diesel/gas
                    #"+1" is added below because option 4 is electric engine. So we are skipping it
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g+1)+"]").click() #ethanol/petrol
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g+1)+"]").click() #gas
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g+1)+"]").click() #other
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g+1)+"]").click() #petrol
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g+1)+"]").click() #petrol and gas
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g+1)+"]").click() #steam                       
                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up 
                    
                    #Loop 4: this is the loop for registration filter
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    for b in range(1,5): #there are 4 registration types
                        if b==1: #first option is omitted as it is the sum of new registration (option 2) and new import (option 3)
                            continue
                      
                        else:
                            time.sleep(1) #waits 1 second before opening the last filter
                            registration_path.location_once_scrolled_into_view #locate the registration block filter
                            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").click() #picks the other registration types options
                
                            #Apply the filters selected
                            #~~~~~~~~~~~~~~~~~~~~~~~~~~
                            driver.find_element_by_xpath("//*[contains(text(), 'Filter Results')]").click() #Once all the filters are setup, then this will close it and show the final results
                            time.sleep(1) # waits 1 second before proceeding to the next line of code
                        
                            #Create the records
                            #~~~~~~~~~~~~~~~~~~
                            create_record_for_csv() #paste the final output in the csv file

                    #Remove the filter from loop 3: engine type
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    time.sleep(1) #waits 1 sec
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter

                    for g1 in range(1,9):
                        driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/div[2]/span/i").click() #unselect the choice in filter
                        driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
   
#********2                
                elif g==4: #electric
                    time.sleep(1)
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div").click() #opens the engine type options that can be selected
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #electric engine                      
                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up 
                    
                    #Loop 4: this is the loop for registration filter
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    for b in range(1,5): #there are 4 registration types
                        if b==1: #first option is omitted as it is the sum of new registration (option 2) and new import (option 3)
                            continue
                      
                        else:
                            time.sleep(1) #waits 1 second before opening the last filter
                            registration_path.location_once_scrolled_into_view #locate the registration block filter
                            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").click() #picks the other registration types options
                
                            #Apply the filters selected
                            #~~~~~~~~~~~~~~~~~~~~~~~~~~
                            driver.find_element_by_xpath("//*[contains(text(), 'Filter Results')]").click() #Once all the filters are setup, then this will close it and show the final results
                            time.sleep(1) # waits 1 second before proceeding to the next line of code
                        
                            #Create the records
                            #~~~~~~~~~~~~~~~~~~
                            create_record_for_csv() #paste the final output in the csv file
 

                    #Remove the filter from loop 3: engine type
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    time.sleep(1) #waits 1 sec
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter

                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/div[2]/span/i").click() #unselect the choice in filter 
                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up
            
 #********3                
                elif g==12: #hybrid
                    time.sleep(1)
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div").click() #opens the engine type options that can be selected
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #diesel/electric
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #diesel/plug-in electric hybrid
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #petrol electric
                    driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/ul/li["+str(g)+"]").click() #petrol/plug-in electric hybrid
                    driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up 
                    
                    #Loop 4: this is the loop for registration filter
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    for b in range(1,5): #there are 4 registration types
                        if b==1: #first option is omitted as it is the sum of new registration (option 2) and new import (option 3)
                            continue
                      
                        else:
                            time.sleep(1) #waits 1 second before opening the last filter
                            registration_path.location_once_scrolled_into_view #locate the registration block filter
                            driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/select/option["+str(b)+"]").click() #picks the other registration types options
                
                            #Apply the filters selected
                            #~~~~~~~~~~~~~~~~~~~~~~~~~~
                            driver.find_element_by_xpath("//*[contains(text(), 'Filter Results')]").click() #Once all the filters are setup, then this will close it and show the final results
                            time.sleep(1) # waits 1 second before proceeding to the next line of code
                        
                            #Create the records
                            #~~~~~~~~~~~~~~~~~~
                            create_record_for_csv() #paste the final output in the csv file

                    #Remove the filter from loop 3: engine type
                    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    time.sleep(1) #waits 1 sec
                    vehicle_path.location_once_scrolled_into_view #locate the vehicle block filter

                    for g2 in range(1,5):
                        driver.find_element_by_xpath("//div/div[4]/div[2]/div/div[1]/div[3]/div[2]/div[5]/div/div[2]/span/i").click() #unselect the choice in filter
                        driver.find_element_by_xpath("//div/div[4]").click() #a trick needed so that the next dropdown can be picked up 

 #********                                
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

#==========================================================================================================
#PART VIII: CLOSE AND DELETE THE JUNK FILE
#_________________________________________
junk.close() #closes the junk file
os.remove('C:\\Users\\alain\\Documents\\NCI\\1st semester\\Database and analytics\\project\\junk_summary.csv') #delete the junk file