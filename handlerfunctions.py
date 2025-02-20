from riderclass import Rider
from driverclass import Driver as d
from  simulation  import Simulation
import csv 
def rider_arrival(sim_instance : Simulation):
    """
    when a new rider arrives, we add them to the system, and start checking whether there are any available drivers to associate them with.
    """
    sim_instance.riders.append(Rider( sim_instance.distributions["location"](), sim_instance.distributions["location"]() , sim_instance) )
    sim_instance.total_riders += 1 #create a new rider object
    rider =  sim_instance.riders[-1]
    sim_instance.riders_system_size += 1    #add the rider to the system size
    current_best_distance = float("inf")    #check whether there is possible assignment
    driver = None  #place holder
    if sim_instance.drivers != [] :  # find if there is already an available driver , else start the wait 
        for i in sim_instance.drivers :  
            if (i.is_available) and (i.calculate_distance(i.location, rider.pickup_location)) < current_best_distance: 
                driver = i # assign the potential driver 
                current_best_distance = i.calculate_distance(i.location, rider.pickup_location) #define the pickup distance
    time = sim_instance.current_time
    if driver:
        Rider.assign_driver(rider,driver)
        driver.start_ride(rider , time)
        ride_length = time  + sim_instance.distributions["ride_length"](driver.expected_trip_time)  
        sim_instance.add_event(ride_length, "rider_departure"  , rider)
        sim_instance.add_event(ride_length , "driver_finish" , driver)
    else:
        sim_instance.add_event(time + sim_instance.distributions["abandomnent"]() , "rider_departure" ,rider) # i have to add the next event as abondement

def rider_departure(sim_instance : Simulation , r1 : Rider ):
    """
    when a rider leave, we drop them from the list of riders waiting in the system , and based on the type of the departure, we update the objects and get the associated metrics
    """
    #check if they abandoned or finished
    if  r1.status == "Waiting": # if the rider abandon the system based on the event calendar
        r1.abandon_ride() 
        sim_instance.abandonment += 1 
        print("abondended")
        sim_instance.rider_csv.append([r1.id , r1.pickup_location , r1.drop_location , r1.status , r1.wait_start_time , "" , "" ])
    else:
        r1.complete_ride()
        print("completed")
        sim_instance.rider_csv.append([r1.id , r1.pickup_location , r1.drop_location , r1.status , r1.wait_start_time , "" , r1.drop_off_time ])
        #sim_instance.average_wait = (sim_instance.average_wait + r1.wait_time ) / 2 
    
    sim_instance.riders.remove(r1) # we drop the object from the list of riders in the system 
    sim_instance.riders_system_size -= 1

def driver_arrival( sim_instance : Simulation):
    """
    when a new driver arrives, we add them as a new object in the list of drivers in the system, and check whether there are riders waiting for assignment 
    """
    #add a new object
    sim_instance.drivers.append(d(sim_instance.distributions["location"]() , sim_instance)) 
    sim_instance.drivers_system_size += 1
    sim_instance.total_drivers += 1 
    driver = sim_instance.drivers[-1]
    driver.log_in()
    sim_instance.add_event(sim_instance.distributions["driver_logout"]()+ sim_instance.current_time , "driver_departure" , driver ) # add the event of the finish in the EC 
    current_best_distance = float("inf")  #check whether there are waiting riders 
    rider = None  #place holder
    if sim_instance.riders != [] : # find if there is already an waiting rider , else start the wait 
        for i in sim_instance.riders :  
            if (i.assigned_driver == None) and (driver.calculate_distance(driver.location, i.pickup_location)) < current_best_distance: 
                rider = i # assign the closest rider
                current_best_distance = driver.calculate_distance(driver.location, i.pickup_location) #define the pickup distance
    if rider:
        time = sim_instance.current_time 
        Rider.assign_driver(rider,driver)
        driver.start_ride(rider , time)
        ride_length = time  + sim_instance.distributions["ride_length"](driver.expected_trip_time) 
        sim_instance.modify_event( "rider_departure",rider,ride_length , "rider_departure"  , rider )
        sim_instance.add_event(ride_length , "driver_finish" , driver)

def driver_departure(sim_instance : Simulation,  driver : d ):
    """
    when a driver gets out of the system, we remove them from the driver_list ( drivers currently in the system), and get all of their relevant statistics 
    """
    if driver.is_available == False : #if he is serving a rider
        sim_instance.modify_event( "driver_finish",driver, driver.ride_end_time, "driver_departure"  , driver ) # he will log out when he finishes the ride 
        sim_instance.driver_csv.append([driver.id , driver.initial_location , driver.log_in_time , driver.log_out_time])
    else : 
        driver.log_out()
        sim_instance.drivers_system_size -= 1 
        sim_instance.driver_csv.append([driver.id , driver.initial_location , driver.log_in_time , driver.log_out_time])
        #sim_instance.average_profit = (driver.profit + sim_instance.average_profit ) /2 
        sim_instance.drivers.remove(driver)
    

def driver_finish( sim_instance : Simulation , driver : d  ): 
    """
    When a drivers finishes from a ride, we mark it as compete, and look whether there are waiting riders
    """
    driver.complete_ride()
    #check whether there are waiting riders 
    current_best_distance = float("inf")  #check whether there are waiting riders 
    rider = None  #place holder
    if sim_instance.riders != [] : # find if there is already an waiting rider , else start the wait 
        for i in sim_instance.riders :  
            if (i.assigned_driver == None) and (driver.calculate_distance(driver.location, i.pickup_location)) < current_best_distance: 
                rider = i # assign the closest rider
                current_best_distance = driver.calculate_distance(driver.location, i.pickup_location) #define the pickup distance
    time = sim_instance.current_time
    if rider:
        Rider.assign_driver(rider,driver)
        driver.start_ride(rider,time)
        ride_length = time  + sim_instance.distributions["ride_length"](driver.expected_trip_time) 
        sim_instance.modify_event( "rider_departure",rider,ride_length , "rider_departure"  , rider )
        sim_instance.add_event(ride_length , "driver_finish" , driver)

def termination( sim_instance: Simulation ):
    print(f"abandonment rate {sim_instance.abandonment/sim_instance.total_riders}")
    print(f"average system size  - drivers {sim_instance.area_drivers_system_size / sim_instance.simulation_length}")
    print(f"average system size  - riders {sim_instance.area_riders_system_size / sim_instance.simulation_length}")
    print(f"total drivers : {sim_instance.total_drivers}")
    print(f"total riders : {sim_instance.total_riders}")
    with open("driver.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Driver_ID", "Initial_Location", "Arrival", "Offline"])
        writer.writerows(sim_instance.driver_csv)
    with open("rider.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Rider_ID", "Initial_Location", "Dropoff_Location", "status", "systemjoin" , "pickup" , "dropoff"])
        writer.writerows(sim_instance.rider_csv)
    print("done")

