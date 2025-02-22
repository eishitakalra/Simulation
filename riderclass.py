import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation import Simulation
    from driverclass import Driver

class Rider:
    i = 1  #track IDs

    def __init__(self,   sim_instance : "Simulation"):
        self.id = f"r{Rider.i}"  # Auto-generate ID
        self.pickup_location =  sim_instance.distributions["location"]()
        self.drop_location =  sim_instance.distributions["location"]()
        Rider.i += 1  # Increment for the next rider

        self.arrival_time = sim_instance.current_time  # Time when the rider requested a ride
        self.driver_assign_time = None
        self.drop_off_time = None
        self.assign_driver = 0
        self.assigned_driver = None  # Driver assigned to the rider
        self.status = "Waiting"  # Waiting, In Ride, Completed, Abandoned
        self.wait_start_time = self.arrival_time  # When the rider started waiting
        self.wait_time = 0  # Total wait time before getting a driver
        self.abandoned = False  # Whether the rider was abandoned
        self.abandonment_time = None  # Time of abandonment
        self.sim_instance= sim_instance
        self.pickup_time = None

    def assign_driver(self, driver : "Driver"):
        """Assign a driver to the rider"""
        self.assigned_driver = driver
        self.driver_assign_time = self.sim_instance.current_time
        self.wait_time = self.driver_assign_time- self.wait_start_time  # Calculate waiting time
        self.status = "In Ride"
        self.pickup_time = driver.ride_start_time
        self.drop_off_time = driver.ride_end_time


    def complete_ride(self):
        """Mark ride as completed."""
        self.status = "Completed"

    def abandon_ride(self):
        """Mark the rider as abandoned if no driver arrives."""
        self.abandoned = True
        self.status = "Abandoned" 


