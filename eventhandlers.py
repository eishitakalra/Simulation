from typing import Any
import handlerfunctions as hf
class EventHandlers :
    def __init__(self, simulation):
        self.simulation = simulation
    def rider_arrival(self,event_data : Any):
        hf.rider_arrival(self.simulation)
    def rider_departure(self,event_data : Any):
        hf.rider_departure(self.simulation)
    def driver_arrival(self,event_data : Any):
        hf.driver_arrival(self.simulation)
    def driver_departure(self, event_data : Any):
        hf.driver_departure(self.simulation)
    def driver_finish(self ,event_data : Any): 
        hf.driver_finish(self.simulation)
    def termination(self,event_data : Any):
        hf.termination(self.simulation)