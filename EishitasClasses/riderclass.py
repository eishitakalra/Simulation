import time

class Rider:
    def __init__(self, rider_id, pickup_location, drop_location):
        self.rider_id = rider_id
        self.pickup_location = pickup_location
        self.drop_location = drop_location

        self.arrival_time = time.time()  # Time when the rider requested a ride
        self.driver_assign_time = None
        self.drop_off_time = None

        self.assigned_driver = None  # Driver assigned to the rider
        self.status = "Waiting"  # Waiting, In Ride, Completed, Abandoned
        self.wait_start_time = self.arrival_time  # When the rider started waiting
        self.wait_time = 0  # Total wait time before getting a driver
        self.abandoned = False  # Whether the rider was abandoned
        self.abandonment_time = None  # Time of abandonment

    def assign_driver(self, driver):
        """Assign a driver to the rider"""
        self.assigned_driver = driver
        self.wait_time = time.time() - self.wait_start_time  # Calculate waiting time
        self.status = "In Ride"
        self.driver_assign_time = time.time()
        self.drop_off_time = driver.ride_end_time


    def complete_ride(self):
        """Mark ride as completed."""
        self.status = "Completed"

    def abandon_ride(self):
        """Mark the rider as abandoned if no driver arrives."""
        self.abandoned = True
        self.status = "Abandoned" 


