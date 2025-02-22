import time
import math
import distributionsclass as dc
from riderclass import Rider
# from  simulation  import Simulation
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
class Driver:
    i = 1  #id_counter
    def __init__(self, location , sim_instance : "Simulation"):
        self.id = f"d{Driver.i}"  # have the ids in format d1 , d2 ... 
        Driver.i += 1 # incrementing the i to be ready for the next id 
        self.initial_location = location  #initial location 
        self.location = location  # current location 
        self.is_available = True 
       
        #time related metrics
        self.busy_time = 0  
        self.free_time = 0  
        self.log_in_time = sim_instance.current_time #when we create the object  
        self.log_out_time_expected = sim_instance.distributions["driver_logout"]()+ self.log_in_time
        self.log_out_time = None
        self.ride_start_time = None  
        self.expected_trip_time = None
        self.ride_end_time = None
        # kpi related stuff
        self.sim_instance = sim_instance
        self.clients = 0 
        self.profit = 0.00 #profit made 
    def calculate_distance(self, location1, location2):
        """Calculate Euclidean distance between two locations."""
        return math.sqrt((location1[0]-location2[0])**2 + (location1[1]-location2[1])**2)

    def log_in(self):
        """Log in the driver and start tracking free time."""
        self.is_available = True
        self.log_in_time = self.sim_instance.current_time  # Store the current time

    def log_out(self):
        """Log out the driver and stop tracking time."""
        self.log_out_time = self.sim_instance.current_time
        session = self.log_out_time - self.log_in_time
        self.free_time += session - self.busy_time  # Calculate free time
        self.is_available = False
        if self.clients == 0 : 
            print(self.id)
        

    def start_ride(self, rider : Rider,   initial_charge = 3, fare_per_mile=2, fuel_cost = 0.2):
        """Assign a ride, move the driver, and start tracking busy time."""
        self.expected_trip_time = self.calculate_distance(rider.pickup_location , rider.drop_location)/20
        ride_distance = self.calculate_distance(rider.pickup_location, rider.drop_location)
        pickup_distance = self.calculate_distance(self.location, rider.pickup_location)
        # Driver is now busy
        self.is_available = False 
        time_until_reach_rider = (pickup_distance/20) 
        # wa9tech tabda el ride ? tabda wakt el driver yousel ll rider
        self.ride_start_time = self.sim_instance.current_time + time_until_reach_rider # Mark ride start time by taking account the time it takes the drives to arrive
        # wa9t erre7la dépend mel distribution , donc lzemni ndakhel el distribution generated ka parameter
        self.trip_time = self.sim_instance.distributions["ride_length"]((self.expected_trip_time))
        #toufa erre7la baaed ma nhabtou el client 
        self.ride_end_time = self.ride_start_time + self.trip_time 
        #ne7sbou el profit melli bde yet7arrek lin w9ef 
        self.profit += initial_charge + fare_per_mile*(ride_distance) - fuel_cost*(ride_distance + pickup_distance)
        #9adech 93adt busy : melli jetni el requestion lin habat el client
        self.busy_time += self.trip_time + time_until_reach_rider  
        self.location = rider.drop_location  # Update location
        self.clients += 1 


    def complete_ride(self):
        """Mark ride as completed, track busy time, and free the driver."""
        # self.busy_time += self.sim_instance.current_time - self.ride_start_time  # Add busy time
        self.is_available = True  # Driver is now free
        self.ride_start_time = None
        self.trip_time = None
        self.expected_trip_time = None
        self.ride_end_time = None
