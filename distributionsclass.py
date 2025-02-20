import random 
class Distributions:
    def __init__(self, simulation):
        self.simulation = simulation
    
    def driver_interarrival(self)->float:
        rate = 3  # λ (rate parameter)
        driver_interarrival_time = random.expovariate(rate)  # Generate exponential RV IN MINUTES
        return driver_interarrival_time

    def rider_interarrival(self)->float:
        rate = 30  # λ (rate parameter)
        rider_interarrival_time = random.expovariate(rate)  # Generate exponential RV IN MINUTES
        return rider_interarrival_time
    
    def driver_log_out(self) -> float:
        log_out_time = random.uniform(5, 8)  # Random time between 5 and 8 hours
        return log_out_time

    def rider_abandonment(self) -> float:
        rate = 5
        rider_abandonment = random.expovariate(rate) #IN MINUTES
        return rider_abandonment
    
    def generate_location(self)->float:
        x = random.uniform(0, 20)
        y = random.uniform(0, 20)
        coordinates = [x, y]
        return coordinates
    
    def generate_ride_length(self, expected_trip_time : float)->float:
        u = expected_trip_time #trip time in minutes
        ride_length = random.uniform(0.8*u, 1.2*u)  # Random time between 5 and 8 hours
        return ride_length
    