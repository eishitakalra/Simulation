from riderclass import Rider
from driverclass import Driver as d
from  distributionsclass import Distributions 
from  simulation  import Simulation
def rider_arrival(sim_instance : Simulation):
    """
    when a new rider arrives, we add them to the system, and start checking whether there are any available drivers to associate them with.
    """
    #create a new rider object
    sim_instance.riders.append(Rider( sim_instance.distributions["location"](), sim_instance.distributions["location"]()) )
    #add the rider to the system size
    sim_instance.riders_system_size += 1    
    #check whether there is possible assignment
    current_best_distance = float("inf")
    driver = None  #place holder
    # find if there is already an available driver , else start the wait 
    # In driver_arrival, find the closest rider

    if sim_instance.drivers != [] : 
        for i in sim_instance.drivers :  
            if (i.is_available) and (i.calculate_distance(i.location, sim_instance.riders[-1].pickup_location)) < current_best_distance: 
                driver = i # assign the potential driver 
                current_best_distance = i.calculate_distance(i.location, sim_instance.riders[-1].pickup_location) #define the pickup distance
    if driver:
        Rider.assign_driver(sim_instance.riders[-1],driver)
        driver.start_ride(sim_instance.riders[-1])
        sim_instance.add_event(sim_instance.current_time  + sim_instance.distributions["ride_length"](driver.expected_trip_time) , "rider_departure"  , sim_instance.riders[-1])
        sim_instance.add_event(sim_instance.current_time + sim_instance.distributions["ride_length"](driver.expected_trip_time) , "driver_finish" , driver)
    else:
        sim_instance.add_event(sim_instance.current_time + sim_instance.distributions["abandomnent"]() , "rider_departure" , sim_instance.riders[-1]) # i have to add the next event as abondement

def rider_departure(sim_instance : Simulation , r1 : Rider ):
    """
    when a rider leave, we drop them from the list of riders waiting in the system , and based on the type of the departure, we update the objects and get the associated metrics
    """
    sim_instance.riders.remove(r1) # we drop the object from the list of riders in the system 
    sim_instance.riders_system_size -= 1
    #check if they abandoned or finished
    if  r1.status == "waiting": # if the rider abandon the system based on the event calendar
        r1.abandon_ride() 
        print("abondended")
    else:
        r1.complete_ride()
        print("completed")
        #sim_instance.average_wait = (sim_instance.average_wait + r1.wait_time ) / 2 

def driver_arrival( sim_instance : Simulation):
    """
    when a new driver arrives, we add them as a new object in the list of drivers in the system, and check whether there are riders waiting for assignment 
    """
    #add a new object
    sim_instance.drivers.append(d(sim_instance.distributions["location"]() , sim_instance)) 
    sim_instance.drivers_system_size += 1
    sim_instance.drivers[-1].log_in()

    # add the event of the finish in the EC 
    sim_instance.add_event(sim_instance.distributions["driver_logout"]()+ sim_instance.current_time , "driver_departure")

    #check whether there are waiting riders 
    current_best_distance = float("inf")
    rider = None  #place holder
    # find if there is already an available driver , else start the wait 
    if sim_instance.riders != [] : 
        for i in sim_instance.riders :  
            if (i.assigned_driver == None) and (sim_instance.drivers[-1].calculate_distance(sim_instance.drivers[-1].location, i.pickup_location)) < current_best_distance: 
                rider = i # assign the closest rider
                current_best_distance = sim_instance.drivers[-1].calculate_distance(sim_instance.drivers[-1].location, i.pickup_location) #define the pickup distance
    if rider:
        Rider.assign_driver(rider,sim_instance.drivers[-1])
        sim_instance.drivers[-1].start_ride(rider)
        sim_instance.add_event(sim_instance.current_time + sim_instance.distributions["ride_length"](sim_instance.drivers[-1].expected_trip_time), "driver_finish")

def driver_departure( driver : d, sim_instance : Simulation):
    """
    when a driver gets out of the system, we remove them from the driver_list ( drivers currently in the system), and get all of their relevant statistics 
    """
    sim_instance.drivers_system_size -= 1 
    sim_instance.average_profit = (driver.profit + sim_instance.average_profit ) /2 
    sim_instance.drivers_list.drop(driver)
    driver.log_out()

def driver_finish( driver : d  ,  sim_instance : Simulation): 
    """
    When a drivers finishes from a ride, we mark it as compete, and look whether there are waiting riders
    """
    driver.complete_ride()
    #check whether there are waiting riders 
    current_best_distance = 10000 
    rider = None  #place holder
    # find if there is already an available driver , else start the wait 
    if sim_instance.riders != [] : 
        for i in sim_instance.riders :  
            if (i.assigned_driver == None) and (sim_instance.drivers[-1].calculate_distance(sim_instance.drivers[-1].location, i.pickup_location)) < current_best_distance: 
                rider = i # assign the closest rider
                current_best_distance = sim_instance.drivers[-1].calculate_distance(sim_instance.drivers[-1].location, i.pickup_location) #define the pickup distance
    if rider:
        Rider.assign_driver(rider,driver)
        sim_instance.drivers[-1].start_ride(rider)
        #ADD TO THE EC THE FINISH OF THE RIDE 
        sim_instance.add_event(sim_instance.current_time  + sim_instance.distributions["ride_length"](driver.expected_trip_time) , "driver_finish")
        sim_instance.add_event(sim_instance.current_time +  sim_instance.distributions["ride_length"](driver.expected_trip_time) , "rider_finish")

def termination( sim_instance: Simulation ):
    #print(f"Average Driver's profit is {sim_instance.area_system_size/sim_instance.simulation_length}")
    print("done")

