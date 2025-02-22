from typing import Any
import handlerfunctions as hf
from driverclass import Driver
from riderclass import Rider
class EventHandlers :
    def __init__(self, simulation):
        self.simulation = simulation
    def rider_arrival(self,event_data : Rider):
        hf.rider_arrival(self.simulation)
    def rider_departure(self,event_data : Rider):
        hf.rider_departure(self.simulation, event_data)
    def driver_arrival(self,event_data : Driver):
        hf.driver_arrival(self.simulation)
    def driver_departure(self, event_data : Driver):
        hf.driver_departure(self.simulation, event_data)
    def driver_finish(self ,event_data : Driver): 
        hf.driver_finish(self.simulation, event_data)
    def termination(self,event_data : Any):
        hf.termination(self.simulation)