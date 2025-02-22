from simulation import Simulation
from distributionsclass import Distributions
from eventhandlers import EventHandlers
import graphs as g


def main():
    handlers = EventHandlers(None)
    distributions = Distributions(None)
    t = 4800
    sim = Simulation(handlers, t, distributions)
    
    handlers.simulation = sim
    distributions.simulation = sim
    
    sim.run()
    g.barplot(sim.clients, "number of clients" , "count of clients","clients distribution" )
    g.cdfplot(sim.profit, "total profit per driving session" , "count " ," profit distribution cdf") 
    g.cdfplot(sim.waiting_time, "" , "","waiting time cdf" ) 
    g.cdfplot(sim.rest_time, "" , "" ,"rest time cdf") 
    g.scatterplot(sim.clients, sim.profit, "Number of Clients", "Total Profit", "Clients vs. Profit")
    g.histplot(sim.profit, "Total Profit", "Frequency", "Profit Distribution")
    g.histplot(sim.waiting_time, "Total waiting time", "Frequency", "waiting time Distribution")
    g.histplot(sim.rest_time, "Total Rest time", "Frequency", "Rest Time Distribution")

    
    
    
if __name__ == "__main__":
    main()
