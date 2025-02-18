from simulation import Simulation
from distributionsclass import Distributions
from eventhandlers import EventHandlers



def main():
    handlers = EventHandlers(None)
    distributions = Distributions(None)
    
    sim = Simulation(handlers, distributions)
    
    handlers.simulation = sim
    distributions.simulation = sim
    
    sim.run()
    
    
    
if __name__ == "__main__":
    main()
