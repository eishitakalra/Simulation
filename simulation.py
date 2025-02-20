from typing import Callable, List, Dict, Any # We need to initialize the elemends of the class and this helps us to do that. 
from bisect import bisect_right
import distributionsclass as dc
from riderclass import Rider
from driverclass import Driver

print("simulation.py loaded successfully")

class Simulation:
    def __init__(self, handlers, distributions: Any = None):
        self.simulation_length = 24 # Termination time
        self.current_time = 0         # Keep tracks of simulation clock
        self.drivers_system_size = 0          # Keeps track of Q_D(t)
        self.riders_system_size = 0          # Keeps track of Q_R(t)
        self.area_drivers_system_size = 0 # AQ_D(t)
        self.area_riders_system_size = 0  # AR_D(t)
        self.total_riders =0 
        self.total_drivers = 0 
        self.profit = [] #avergae profit per driver 
        self.waiting_time = [] #average waiting time ( riders ) 
        self.rest_time = [] #average rest time (drivers) 
        self.abandonment = 0 # number of people abandonning the system 
        
        self.event_calendar: List[Dict[str, Any , Any]] = [] # Event calendar is initialized as empty the structure : str: event type, Any : time , Any: driver/rider object
        self.distributions: Dict[str, Callable[[Any], None]] = {} 
        self.event_handlers: Dict[str, Callable[[Any], None]] = {} # The event_handlers list will associate each event with the modules/functions necessary to execute that event. This list is empty and designed to be dynamic to flexiblity add or remove event types.
        self.riders : List[Rider] = []
        self.drivers : List[Driver] = []
        self.driver_csv = []
        self.rider_csv = []

        if distributions:
            self.register_distribution("driver_inter-arrival", distributions.driver_interarrival)
            self.register_distribution("rider_inter-arrival", distributions.rider_interarrival)
            self.register_distribution("location", distributions.generate_location)
            self.register_distribution("ride_length", distributions.generate_ride_length)
            self.register_distribution("driver_logout", distributions.driver_log_out)
            self.register_distribution("abandomnent", distributions.rider_abandonment)
        
        if handlers:
            self.register_event_handler("rider_arrival", handlers.rider_arrival)
            self.register_event_handler("driver_arrival", handlers.driver_arrival)
            self.register_event_handler("driver_departure", handlers.driver_departure)
            self.register_event_handler("rider_departure", handlers.rider_departure)
            self.register_event_handler("driver_finish", handlers.driver_finish)
            self.register_event_handler("termination", handlers.termination)
            
        first_rider_arrival = self.current_time + self.distributions["rider_inter-arrival"]()
        first_driver_arrival = self.current_time + self.distributions["driver_inter-arrival"]()
        self.add_event(first_rider_arrival, "rider_arrival", None)
        self.add_event(first_driver_arrival, "driver_arrival", None)
        self.add_event(self.simulation_length, "termination", None)
        t_d = first_driver_arrival
        t_r = first_rider_arrival
        while t_r < self.simulation_length :
            t_r = self.distributions["rider_inter-arrival"]() + t_r 
            self.add_event(t_r ,"rider_arrival" , None)
        while t_d < self.simulation_length : 
            t_d = self.distributions["driver_inter-arrival"]() + t_d
            self.add_event(t_d ,"driver_arrival" , None)

            
            
        
        
    def add_event(self, event_time:float, event_type: str, event_data: Any =  None )->None:
        event = {'time': event_time, 'type': event_type, 'person': event_data}
        index = bisect_right([e['time'] for e in self.event_calendar], event_time)
        self.event_calendar.insert(index, event)
        
    def modify_event(self, event_type: str, event_data: Any, new_event_time: float, new_event_type: str , new_event_data: Any )-> None:
        """
        Finds an event by type and data, modifies it, and keeps the event calendar sorted.
        """
        for i, event in enumerate(self.event_calendar):
            if event['type'] == event_type and event['person'] == event_data:
                self.event_calendar.pop(i) # Remove the event from the calendar
                updated_event = {'time': new_event_time , 'type': new_event_type , 'person': new_event_data }  # Update the event fields 
                self.add_event(updated_event['time'], updated_event['type'], updated_event['person'])

    def register_distribution(self, random_quantity: str, handler: Callable[[Any], None]):
        self.distributions[random_quantity] = handler
        
        
    def register_event_handler(self, event_type: str, handler: Callable[[Any], None]) -> None:
        # This function allows us to dynamically add event types to the list.
        self.event_handlers[event_type] = handler
        
    def progress_time(self) -> None:
        if not self.event_calendar:
            print("No more events to process.")
            return

        next_event = self.event_calendar.pop(0)
        previous_time = self.current_time
        self.current_time = next_event['time']
        event_type = next_event['type']
        event_data = next_event['person']
        
        self.area_drivers_system_size += self.drivers_system_size*(self.current_time - previous_time)
        self.area_riders_system_size += self.riders_system_size*(self.current_time - previous_time)

        # Open a log file in append mode
        log_file = open(r"\workspaces\Simulation", "a")

        # Process events
        if event_data is None and event_type == "rider_arrival":
            rider_id = self.total_riders + 1
            log_file.write(f"Processing event: {event_type} at time {self.current_time} for person r{rider_id}\n")
        elif event_data is None and event_type == "driver_arrival":
            driver_id = self.total_drivers + 1
            log_file.write(f"Processing event: {event_type} at time {self.current_time} for person d{driver_id}\n")
        elif event_type == "termination":
            log_file.write(f"Processing event: {event_type} at time {self.current_time}\n")
        else:
            log_file.write(f"Processing event: {event_type} at time {self.current_time} for person {event_data.id}\n")

        # Handle event if a handler exists
        if event_type in self.event_handlers:
            self.event_handlers[event_type](event_data)
        else:
            log_file.write(f"No handler registered for event type: {event_type}\n")

        # Close the file after writing
        log_file.close()

            
            
    def run(self) -> None:
        """
        Run the simulation until all events are processed or a 'termination' event is encountered.
        """
        print(self.event_calendar)
        terminate_sim = 0
        while self.event_calendar:
            next_event = self.event_calendar[0]  # Peek at the next event
            if next_event['type'] == "termination":
                terminate_sim = 1
            self.progress_time()
            if terminate_sim == 1:
                break
        if terminate_sim == 0:
            print("No more event to execute!")
            
        
        
            
            
            
        
            
        
        