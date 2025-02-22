from riderclass import Rider
from driverclass import Driver as d
from  simulation  import Simulation
import csv 
import numpy as np
def rider_arrival(sim_instance : Simulation):
    """
    when a new rider arrives, we add them to the system, and start checking whether there are any available drivers to associate them with.
    """
    sim_instance.riders.append(Rider(sim_instance))
    sim_instance.total_riders += 1 #create a new rider object
    rider =  sim_instance.riders[-1]
    sim_instance.riders_system_size += 1    #add the rider to the system size
    current_best_distance = float("inf")    #check whether there is possible assignment
    driver = None  #place holder
    if sim_instance.drivers != [] :  # find if there is already an available driver , else start the wait 
        for i in sim_instance.drivers :  
            if (i.is_available == True) and (i.calculate_distance(i.location, rider.pickup_location)) < current_best_distance: 
                driver = i # assign the potential driver 
                current_best_distance = i.calculate_distance(i.location, rider.pickup_location) #define the pickup distance
    time = sim_instance.current_time
    if driver != None:
        driver.start_ride(rider)
        Rider.assign_driver(rider,driver)
        sim_instance.add_event(driver.ride_end_time, "rider_departure"  , rider)
        sim_instance.add_event(driver.ride_end_time , "driver_finish" , driver)
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
        sim_instance.rider_csv.append([r1.id , r1.pickup_location , r1.drop_location , r1.status , r1.wait_start_time , "" , "" ,""])
    else:
        r1.complete_ride()
        sim_instance.rider_csv.append([r1.id , r1.pickup_location , r1.drop_location , r1.status , r1.wait_start_time , r1.pickup_time , r1.drop_off_time , r1.assigned_driver.id ])
        sim_instance.waiting_time.append(r1.wait_time)
    
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
    sim_instance.add_event(driver.log_out_time_expected , "driver_departure" , driver ) # add the event of the finish in the EC 
    current_best_distance = float("inf")  #check whether there are waiting riders 
    rider = None  #place holder
    if sim_instance.riders != [] : # find if there is already an waiting rider , else start the wait 
        for i in sim_instance.riders :  
            if (i.assigned_driver == None) and (driver.calculate_distance(driver.location, i.pickup_location)) < current_best_distance: 
                rider = i # assign the closest rider
                current_best_distance = driver.calculate_distance(driver.location, i.pickup_location) #define the pickup distance
    if rider != None:
        driver.start_ride(rider)
        Rider.assign_driver(rider,driver)
        sim_instance.modify_event( "rider_departure", rider, driver.ride_end_time , "rider_departure"  , rider )
        sim_instance.add_event(driver.ride_end_time , "driver_finish" , driver)
  
def driver_finish( sim_instance : Simulation , driver : d  ): 
    """
    When a drivers finishes from a ride, we mark it as compete, and look whether there are waiting riders
    """
    driver.complete_ride()
    if driver.log_out_time == sim_instance.current_time : 
        driver_departure(sim_instance , driver)
    else :
        current_best_distance = float("inf")  #check whether there are waiting riders 
        rider = None  #place holder
        if sim_instance.riders != [] : # find if there is already a waiting rider , else start the wait 
            for i in sim_instance.riders :  
                if (i.assigned_driver == None) and (driver.calculate_distance(driver.location, i.pickup_location)) < current_best_distance: 
                    rider = i # assign the closest rider
                    current_best_distance = driver.calculate_distance(driver.location, i.pickup_location) #define the pickup distance
        if rider != None :
            driver.start_ride(rider)
            Rider.assign_driver(rider,driver)
            sim_instance.modify_event( "rider_departure",rider,driver.ride_end_time , "rider_departure"  , rider )
            sim_instance.add_event(driver.ride_end_time , "driver_finish" , driver)

def driver_departure(sim_instance : Simulation,  driver : d ):
    """
    when a driver gets out of the system, we remove them from the driver_list ( drivers currently in the system), and get all of their relevant statistics 
    """
    if driver.ride_end_time != None : #if he is serving a rider
        driver.log_out_time = driver.ride_end_time
        sim_instance.modify_event( "driver_departure" , driver , driver.ride_end_time, "driver_departure"  , driver ) # he will log out when he finishes the ride 
    elif driver.ride_end_time == None : 
        driver.log_out()
        sim_instance.drivers_system_size -= 1 
        sim_instance.driver_csv.append([driver.id , driver.initial_location , driver.log_in_time , driver.log_out_time])
        sim_instance.clients.append(driver.clients)
        sim_instance.profit.append(driver.profit /( driver.log_out_time - driver.log_in_time))
        sim_instance.rest_time.append(driver.free_time )
        sim_instance.rest_mean.append(driver.free_time /(driver.log_out_time - driver.log_in_time))
        sim_instance.drivers.remove(driver)

def termination( sim_instance: Simulation ):

# Open a text file to save the results
    with open("simulation_results.txt", "w") as f:
        # Basic Statistics
        
        f.write("abandonment statistics :\n ")
        f.write(f"Hourly abandonment rate: {sim_instance.abandonment / sim_instance.simulation_length}\n")       
        f.write(f"Abandonment rate: {sim_instance.abandonment / (sim_instance.total_riders- sim_instance.riders_system_size)}\n")
        f.write("Riders numbers:\n " )
        f.write(f"Average number of riders per driving session: {sum(sim_instance.clients)/len(sim_instance.clients) if sim_instance.clients else 0}\n")
        f.write(f"Maximum number of riders per driving session: {max(sim_instance.clients)}\n")
        f.write(f"Minimum number of riders per driving session: {min(sim_instance.clients)}\n")
        f.write(f"Std Dev of riders per session: {np.std(sim_instance.clients)}\n")
        f.write("Earnings:\n " )
        f.write(f"Average earnings per hour: {sum(sim_instance.profit)/len(sim_instance.profit)}\n")
        f.write(f"Maximum of earnings per hour: {np.max(sim_instance.profit)}\n")
        f.write(f"Minimum of earnings per hour: {np.min(sim_instance.profit)}\n")
        f.write(f"Std Dev of earnings per hour: {np.std(sim_instance.profit)}\n")
        f.write("Rest time:\n " )
        f.write(f"Average rest time per session: {sum(sim_instance.rest_time)/len(sim_instance.rest_time)}\n")
        f.write(f"percentage rest time per session : {sum(sim_instance.rest_mean)/len(sim_instance.rest_mean)}\n")
        f.write(f"Std Dev of rest time per session: {np.std(sim_instance.rest_time)}\n")
        f.write("Counts:\n " )
        f.write(f"Total number of drivers: {sim_instance.total_drivers}\n")
        f.write(f"Total number of riders: {sim_instance.total_riders}\n")
        f.write("waiting time:\n " )
        f.write(f"Average waiting time per rider: {sum(sim_instance.waiting_time)/len(sim_instance.waiting_time)}\n")
        f.write(f"Maximum waiting time: {max(sim_instance.waiting_time)}\n")
        f.write(f"Minimum waiting time: {min(sim_instance.waiting_time)}\n")
        f.write(f"Std Dev of waiting time: {np.std(sim_instance.waiting_time)}\n")
        
  

    print("Simulation results saved ")


    with open("driver.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Driver_ID", "Initial_Location", "Arrival", "Offline" ])
        all_drivers = sim_instance.driver_csv + [
        [driver.id, driver.initial_location, driver.log_in_time, driver.log_out_time ]
        for driver in sim_instance.drivers ]
        all_drivers.sort(key=lambda row: row[2])
        writer.writerows(all_drivers)
    with open("rider.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Rider_ID", "Initial_Location", "Dropoff_Location", "status", "systemjoin" , "pickup" , "dropoff","driver"])
        all_riders = sim_instance.rider_csv + [
        [rider.id , rider.pickup_location , rider.drop_location , rider.status , rider.wait_start_time , rider.pickup_time , rider.drop_off_time , ""]  
        for rider in sim_instance.riders ]
        all_riders.sort(key=lambda row: row[4])
        writer.writerows(all_riders)
    print("done")

