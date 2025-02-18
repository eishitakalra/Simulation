import time
import math
import distributionsclass as dc

class Driver:
    i = 1  #id_counter
    def __init__(self, location):
        self.driver_id = f"d{Driver.i}"  # have the ids in format d1 , d2 ... 
        Driver.i += 1 # incrementing the i to be ready for the next id 
        self.location = location  
        self.is_available = True 
        self.profit = 0.00
        self.busy_time = 0  
        self.free_time = 0  
        self.log_in_time = None  
        self.log_out_time = None
        self.ride_start_time = None  
        self.expected_trip_time = None
        self.ride_end_time = None

    def calculate_distance(self, location1, location2):
        """Calculate Euclidean distance between two locations."""
        return math.sqrt((location1[0]-location2[0])**2 + (location1[1]-location2[1])**2)

    def log_in(self):
        """Log in the driver and start tracking free time."""
        self.is_available = True
        self.log_in_time = time.time()  # Store the current time

    def log_out(self):
        """Log out the driver and stop tracking time."""
        self.free_time += time.time() - self.start_time - self.busy_time  # Calculate free time
        self.is_available = False
        self.log_out_time = time.time()

    def start_ride(self, rider, initial_charge = 3, fare_per_mile=2, fuel_cost = 0.2):
        """Assign a ride, move the driver, and start tracking busy time."""
        
        ride_distance = self.calculate_distance(rider.pickup_location, rider.drop_location)
        pickup_distance = self.calculate_distance(self.location, rider.pickup_location)
        self.is_available = False  # Driver is now busy
        self.ride_start_time = time.time()  # Mark ride start time
        self.trip_time = dc.generate_ride_length((ride_distance + pickup_distance)*3)   # IN MINUTES!! mu(t)
        self.ride_end_time = time.time() + self.trip_time # When ride will end
        self.profit += initial_charge + fare_per_mile*(ride_distance) - fuel_cost*(ride_distance + pickup_distance)
        self.busy_time += self.trip_time   # IN MINUTES
        self.location = rider.drop_location  # Update location


    def complete_ride(self):
        """Mark ride as completed, track busy time, and free the driver."""
        self.busy_time += time.time() - self.ride_start_time  # Add busy time
        self.is_available = True  # Driver is now free
        self.ride_start_time = None
        self.trip_time = None
        self.expected_trip_time = None
        self.ride_end_time = None
