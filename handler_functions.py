from simulation import Simulation

def execute_arrival(sim_instance:Simulation):
    # Increment the system size by 1
    sim_instance.system_size += 1
    
    if sim_instance.ATM_state == 0:
        sim_instance.ATM_state = 1
        departure_time = sim_instance.current_time + sim_instance.distributions["service"]()
        sim_instance.add_event(departure_time, "departure", None)
    
    next_arrival_time = sim_instance.current_time + sim_instance.distributions["inter-arrival"]()
    sim_instance.add_event(next_arrival_time, "arrival", None)
    

def execute_departure(sim_instance:Simulation):
    sim_instance.system_size -= 1
    if sim_instance.system_size > 0:
        departure_time = sim_instance.current_time + sim_instance.distributions["service"]()
        sim_instance.add_event(departure_time, "departure", None)
    else:
        sim_instance.ATM_state = 0
    

def execute_termination(sim_instance:Simulation):
    print(f"Average System Size is {sim_instance.area_system_size/sim_instance.simulation_length}")
    print(f"Average Utilization is {sim_instance.area_ATM_state/sim_instance.simulation_length}")
    
        
        
        
    