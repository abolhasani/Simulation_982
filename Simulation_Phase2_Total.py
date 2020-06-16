"""
Simulation of fast-food restaurant
system description should be added
Outputs : 1-mean time for customer being in the system
          2-mean customer's waiting time in receiving food
          3-mean and maximum of queue length in serving food part
          4-mean performance of the servers in ordering and receiving part
          5-mean and maximum of queue length in recieving and ordering food part      
Starting State = ...

Authors: Mohammad Sadegh Abolhasani, Abolfazl Tghavi
Starting Date:9 May 2020
Finishing Date:... May 2020
"""

import random
import math
import pandas as pd
import numpy as np
from operator import itemgetter


# an array for holding the information of all customers attended
customers = []
# defining statistics which should be updated during the simulation
total_time_customer_in_system = 0
total_num_of_exited_customers = 0
total_time_customer_in_receiving_queue = 0
total_num_of_customers_received_food = 0
serving_food_queue_length = []
ordering_queue_length = []
receiving_queue_length = []
total_ordering_server_busy_time = 0
total_receiving_server_busy_time = 0
ordering_servers_rest_time = 0
receiving_servers_rest_time = 0
#the indicator variables which is used fo determining the first customer in each queue
ordering_queue = []
receiving_queue = []
serving_queue = []

# defining a class for customers
class Customer:
    index = 0
    entering_time = 0
    exit_time = 0
    entering_time_to_receiving_section = 0

    def __init__(self, index, enetering_time):
        self.index = index
        self.entering_time = enetering_time


# initialization of the system states and FEL
def starting_state():

    # this clock will be used in the code and it is based on the minutes which is passed till then
    clock = 0
    # this clock has two part: one for hour and the other for minutes and it will start from 10 AM
    Real_clock = dict()
    Real_clock["hour"] = 10
    Real_clock["minute"] = 0

    step = 0

    # State
    state = dict()
    state['Ordering_Server_Idle'] = 5
    state['Ordering_Server_Resting'] = 0
    state['Ordering_Server_Rest_blocked'] = 0
    state['Ordering_queue'] = 0
    state['Receiving_Server_Idle'] = 2
    state['Receiving_Server_Resting'] = 0
    state['Receiving_Server_Rest_blocked'] = 0
    state['Receiving_queue'] = 0
    state['Serving_Chairs_Idle'] = 30
    state['serving_queue'] = 0

    # the initial FEL
    future_event_list = list()
    FEL_maker(future_event_list, ["Event type" , "Event time" ],  ["PCE" , exponential_random_variate(3)])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["CCE" , exponential_random_variate(5)])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["BE" , random_uniform_between(60 , 180)])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 50])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 110])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 230])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 290])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 50])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 110])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 230])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 290])
    return state, future_event_list, step, clock, Real_clock


# a function for making new event notices and adding them to the FEL
def FEL_maker(future_event_list,keys, values):
    new_event = dict()
    for i in range(len(keys)):
        new_event[keys[i]] = values[i]
    future_event_list.append(new_event)

#the functions for generating random numbers

# should be developed by Abolfazl
def triangular_random_variate(a , b , c):
    R = np.random.random()
    h = (c-a)/2
    threshold = (b-a)/(c-a)
    if R < threshold :
        return (np.sqrt((c-a)*(b-a)*R) + a)
    else :
        x = c-a
        y = c-b
        return (c - np.sqrt((1-R)*x*y))

# should be developed by Abolfazl
def poisson_random_variate(mean):
    n = 0
    P = 1
    threshold = np.exp(-mean)
    while (True):
        R = np.random.random()
        P *= R
        if P < threshold:
            return n
        else :
            n += 1

# should be developed by Abolfazl
def num_of_car_passangers():
    R = np.random.random()
    if R < 0.2 :
        return 1
    elif R < 0.5 :
        return 2
    elif R < 0.8 :
        return 3
    else :
        return 4

# should be developed by Mohammad Sadegh
def exponential_random_variate(mean):
   #Based on Slide 8.1
   rand = random.random()
   exp = math.log(rand)
   erv = -1*mean*exp
   return erv

# should be developed by Mohammad Sadegh
def random_uniform_between(min, max):
    #Based on Slide 8.1
    rand = random.random()
    range = max - min
    uni = min + range*rand
    return uni

#the functions for events

# Pedestrian Customer Entrance
# should be developed by Abolfazl
def PCE(future_event_list, state, clock , customers):
    #appending the next PCE event to the FEL
    FEL_maker(future_event_list, ["Event type" , "Event time"], ["PCE" , clock + exponential_random_variate(3)])
    #instantiating a new customer and appendign it to the list of customers
    customer_index = len(customers)
    customer = Customer(customer_index, clock)
    customers.append(customer)

    if state["Ordering_Server_Idle"] == 0:
        state["Ordering_queue"] += 1
        global ordering_queue
        ordering_queue.append(customers[customer_index])
    else :
        state["Ordering_Server_Idle"] -= 1
        #random variates for determining time of ordering process and paying the money
        ordering = triangular_random_variate(1, 2, 4)
        paying_money = triangular_random_variate(1, 2, 3)
        FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , customer_index])
        #updating the cumulative statistics
        global total_ordering_server_busy_time
        total_ordering_server_busy_time += ordering + paying_money

# Car Customer Enterance
# should be developed by Abolfazl
def CCE(future_event_list, state, clock, customers):
    #appending the next CCE event to the FEL
    FEL_maker(future_event_list, ["Event type" , "Event time"], ["CCE" , clock + exponential_random_variate(5)])
    #generating random variate for number of car passangers
    G = num_of_car_passangers()
    for i in range(G):
        customer_index = len(customers)
        #instantiating a new customer and appendign it to the list of customers
        customer = Customer(customer_index, clock)
        customers.append(customer)
        if state["Ordering_Server_Idle"] == 0:
            state["Ordering_queue"] += 1
            global ordering_queue
            ordering_queue.append(customers[customer_index])
        else :
            state["Ordering_Server_Idle"] -= 1
            #random variates for determining time of ordering process and paying the money
            ordering = triangular_random_variate(1, 2, 4)
            paying_money = triangular_random_variate(1, 2, 3)
            FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , customer_index])
            #updating the cumulative statistics
            global total_ordering_server_busy_time
            total_ordering_server_busy_time += ordering + paying_money



# Bus Entrance
# should be developed by Mohammad Sadegh
def BE(future_event_list, state, clock, customers):
    p = int(poisson_random_variate(30))
    for i in range(p):
        customer_index = len(customers)
        # instantiating a new customer and appending it to the list of customers
        customer = Customer(customer_index, clock)
        customers.append(customer)
        if state["Ordering_Server_Idle"] == 0:
            state["Ordering_queue"] += 1
            global ordering_queue
            ordering_queue.append(customers[customer_index])
        else:
            state["Ordering_Server_Idle"] -= 1
            # random variates for determining time of ordering process and paying the money
            ordering = triangular_random_variate(1, 2, 4)
            paying_money = triangular_random_variate(1, 2, 3)
            FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"], ["OF", clock + ordering + paying_money, customer_index])
            # updating the cumulative statistics
            global total_ordering_server_busy_time
            total_ordering_server_busy_time +=  ordering + paying_money


# Ordering Finish
# should be developed by Mohammad Sadegh
def OF(future_event_list, state, clock, customer_index):
    if state["Ordering_Server_Rest_blocked"] == 1:
        state["Ordering_Server_Rest_blocked"] = 0
        state['Ordering_Server_Resting'] += 1
        FEL_maker(future_event_list, ["Event type", "Event time"], ["OSRF", clock + 10])
    going_to_receive = exponential_random_variate(0.5)
    FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],["RE", clock + going_to_receive, customer_index])
    if state["Ordering_queue"] == 0:
        state["Ordering_Server_Idle"] += 1
    else:
        state["Ordering_queue"] -= 1
        # random variates for determining time of ordering process and paying the money
        ordering = triangular_random_variate(1, 2, 4)
        paying_money = triangular_random_variate(1, 2, 3)
        global ordering_queue
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"], ["OF", clock + ordering + paying_money, ordering_queue[0].index])
        ordering_queue.remove(ordering_queue[0])
        # updating the cumulative statistics
        global total_ordering_server_busy_time 
        total_ordering_server_busy_time += ordering + paying_money


# Receiving Entrance
# should be developed by Mohammad Sadegh
def RE(future_event_list, state, clock, customers, customer_index):
    if state["Receiving_Server_Idle"] == 0:
        state["Receiving_queue"] += 1
        global receiving_queue
        receiving_queue.append(customers[customer_index])
        #total_time_customer_in_receiving_queue += clock - customers[customer_index].entering_receiving_section_time
    else:
        state["Receiving_Server_Idle"] -= 1
        # random variates for determining time of ordering process and paying the money
        receiving = random_uniform_between(0.5,2)
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],["RF", clock + receiving, customer_index])
        customers[customer_index].entering_receiving_section_time = clock
        # updating the cumulative statistics
        global total_receiving_server_busy_time
        total_receiving_server_busy_time += receiving
    #updating the cumulative statistics
    customers[customer_index].entering_time_to_receiving_section = clock

# Receiving Finish
# should be developed by Abolfazl
def RF(future_event_list, state, clock ,customers , customer_index):
    #this part should be completed after abol's part
    FEL_maker(future_event_list,["Event type" , "Event time" , "Customer index"], ["SE" , clock + exponential_random_variate(0.5) , customer_index])
    if state['Receiving_Server_Rest_blocked'] == 1 :
        state['Receiving_Server_Rest_blocked'] = 0
        state['Receiving_Server_Resting'] += 1
    if  state['Receiving_queue'] == 0 :
        state['Receiving_Server_Idle'] += 1
    else :
        state['Receiving_queue'] -= 1
        receiving = random_uniform_between(0.5,2)
        global receiving_queue
        FEL_maker(future_event_list,["Event type" , "Event time" , "Customer index"], ["RF" , clock + receiving , receiving_queue[0].index])
        receiving_queue.remove(receiving_queue[0])
        #updating the cumulative statistics
        global total_receiving_server_busy_time
        total_receiving_server_busy_time += receiving
    #updating the cumulative statistics
    global total_time_customer_in_receiving_queue
    global total_num_of_customers_received_food 
    total_time_customer_in_receiving_queue += (clock - customers[customer_index].entering_time_to_receiving_section)
    total_num_of_customers_received_food += 1


# Serving Entrance
# should be developed by Mohammad Sadegh
def SE(future_event_list, state, clock, customer_index):
    if state["Serving_Chairs_Idle"] == 0:
        state["serving_queue"] += 1
        global serving_queue
        serving_queue.append(customers[customer_index])
    else:
        state["Serving_Chairs_Idle"] -= 1
        # random variates for determining time of ordering process and paying the money
        serving = triangular_random_variate(10, 20, 30)
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"], ["SF", clock + serving, customer_index])
    # updating the cumulative statistics
    # there is no need to update the cumulative statistics here


# Serving Finish
# should be developed by Mohammad Sadegh
def SF(future_event_list, state, clock, customer_index):
    exiting = exponential_random_variate(1)
    FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"], ["E", clock + exiting, customer_index])
    if state["serving_queue"] == 0:
        state["Serving_Chairs_Idle"] += 1
    else:
        state["serving_queue"] -= 1
        # random variates for determining time of ordering process and paying the money
        serving = triangular_random_variate(10, 20, 30)
        global serving_queue
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"], ["SF", clock + serving, serving_queue[0].index])
        serving_queue.remove(serving_queue[0])
    # updating the cumulative statistics
    # there is no need to update the cumulative statistics here



# Exit
# should be developed by Abolfazl
def E(clock , customers , customer_index):
    # updating the cumulative statistics
    global total_time_customer_in_system
    global total_num_of_exited_customers 
    total_time_customer_in_system += (clock - customers[customer_index].entering_time)
    total_num_of_exited_customers += 1
    return 0



# Ordering Server Rest Start
# should be developed by Mohammad Sadegh
def OSRS(future_event_list, state, clock):
    if state["Ordering_Server_Idle"] == 0:
        state["Ordering_Server_Rest_blocked"] += 1
    else:
        state["Ordering_Server_Resting"] += 1
        FEL_maker(future_event_list, ["Event type", "Event time"], ["OSRF", clock + 10 ])

# Ordering Server Rest Finish
# should be developed by Abolfazl
def OSRF(future_event_list, state, clock ):
    state['Ordering_Server_Resting'] = 0
    if state['Ordering_queue'] == 0:
        state['Ordering_Server_Idle'] += 1
    else:
        state['Ordering_queue'] -= 1
        #random variates for determining time of ordering process and paying the money
        ordering = triangular_random_variate(1, 2, 4)
        paying_money = triangular_random_variate(1, 2, 3)
        #this should be completed when the OF event developed
        global ordering_queue
        FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , ordering_queue[0].index])
        ordering_queue.remove(ordering_queue[0])
        # updating the cumulative statistics
        global total_ordering_server_busy_time
        total_ordering_server_busy_time +=  ordering + paying_money
    #updating the cumulative statistics
    global ordering_servers_rest_time
    ordering_servers_rest_time += 10


# Receiving Server Rest Start
# should be developed by Abolfazl
def RSRS(future_event_list, state, clock):
    if state['Receiving_Server_Idle'] == 0:
        state['Receiving_Server_Rest_blocked'] += 1
    else:
        state['Receiving_Server_Resting'] += 1
        FEL_maker(future_event_list, ["Event type" , "Event time"], ["RSRF" , clock + 10])

# Receiving Server Rest Finish
# should be developed by Abolfazl
def RSRF(future_event_list, state, clock):
    state['Receiving_Server_Resting'] = 0
    if state['Receiving_queue'] == 0:
        state['Receiving_Server_Idle'] += 1
    else:
        state['Receiving_queue'] -= 1
        #random variates for determining time of receiving the ordered food
        receiving = random_uniform_between(0.5,2)
        #this should be completed when the OF event developed
        global receiving_queue
        FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["RF" , clock + receiving , receiving_queue[0].index])
        receiving_queue.remove(receiving_queue[0])   
    #updating the cumulative statistics
    global receiving_servers_rest_time
    receiving_servers_rest_time += 10

def update_Real_clock(Real_clock, clock):
    Real_clock["minute"] = clock % 60
    Real_clock["hour"] = 10 + int(clock/60)

def update(output_tracking_table, Real_clock, current_event, state, step):

    new_row = dict()
    new_row["clock"] = Real_clock
    new_row["current event type"] = current_event['Event type']
    new_row["Ordering_Server_Idle"] = state['Ordering_Server_Idle']
    new_row["Ordering_Server_Resting"] = state['Ordering_Server_Resting']
    new_row["Ordering_Server_Rest_blocked"] = state['Ordering_Server_Rest_blocked']
    new_row["Ordering_queue"] = state['Ordering_queue']
    new_row["Receiving_Server_Idle"] = state['Receiving_Server_Idle']
    new_row["Receiving_Server_Resting"] = state['Receiving_Server_Resting']
    new_row["Receiving_Server_Rest_blocked"] = state['Receiving_Server_Rest_blocked']
    new_row["Receiving_queue"] = state['Receiving_queue']
    new_row["Serving_Chairs_Idle"] = state['Serving_Chairs_Idle']
    new_row["serving_queue"] = state['serving_queue']
    new_row["total_time_customer_in_system"] = total_time_customer_in_system
    new_row["total_num_of_exited_customers"] = total_num_of_exited_customers
    new_row["total_time_customer_in_receiving_queue"] = total_time_customer_in_receiving_queue
    new_row["total_num_of_customers_received_food"] = total_num_of_customers_received_food
    new_row["serving_food_queue_length"] = serving_food_queue_length[step-1]
    new_row["total_ordering_server_busy_time"] = total_ordering_server_busy_time
    new_row["total_receiving_server_busy_time"] = total_receiving_server_busy_time
    new_row["ordering_servers_rest_time"] = ordering_servers_rest_time
    new_row["receiving_servers_rest_time"] = receiving_servers_rest_time
    #append row to the dataframe
    output_tracking_table = output_tracking_table.append(new_row, ignore_index=True)
    return output_tracking_table



# should be developed by Abolfazl
def simulation(simulation_time):
    output_tracking_table = pd.DataFrame(columns=["clock", "current event type", "Ordering_Server_Idle", "Ordering_Server_Resting" , "Ordering_Server_Rest_blocked",
    "Ordering_queue" , "Receiving_Server_Idle" , "Receiving_Server_Resting" , "Receiving_Server_Rest_blocked", "Receiving_queue" , "Serving_Chairs_Idle" ,
    "serving_queue" , "total_time_customer_in_system", "total_time_customer_in_system","total_num_of_exited_customers","total_time_customer_in_receiving_queue",
    "total_num_of_customers_received_food","serving_food_queue_length","total_ordering_server_busy_time", "total_receiving_server_busy_time" , "ordering_servers_rest_time",
    "receiving_servers_rest_time" ])

    state, future_event_list , step, clock, Real_clock = starting_state()

    future_event_list.append({'Event type': 'End of Simulation', 'Event time': simulation_time})

    while clock < simulation_time:
        sorted_fel = sorted(future_event_list, key=lambda x: x['Event time'])
        """
        print(step)
        print("ordering_queue")
        for i in range(len(ordering_queue)):
            print(ordering_queue[i].index)
        print("receiving_queue")
        for i in range(len(receiving_queue)):
            print(receiving_queue[i].index)
        """
        print("OSI" , state['Ordering_Server_Idle'])
        print("OSR" , state['Ordering_Server_Resting'])
        print("OSRB" , state['Ordering_Server_Rest_blocked'])
        print("OQ" , state['Ordering_queue'])
        print("RSI" , state['Receiving_Server_Idle'])
        print("RSR" , state['Receiving_Server_Resting'])
        print("RSRB" , state['Receiving_Server_Rest_blocked'])
        print("RQ" , state['Receiving_queue'])
        print("SCI" , state['Serving_Chairs_Idle'])
        print(state['serving_queue'])
        """"
        for i in range(len(customers)):
            print("customer" , customers[i].index)
            print(customers[i].entering_time_to_receiving_section)
        """
        print(sorted_fel)
        step += 1
        current_event = sorted_fel[0]
        clock = current_event['Event time']
        update_Real_clock(Real_clock, clock)

        if clock < simulation_time:
            if current_event['Event type'] == 'PCE':
                PCE(future_event_list, state, clock , customers)
            elif current_event['Event type'] == 'CCE':
                CCE(future_event_list, state, clock , customers)
            elif current_event['Event type'] == 'BE':
                BE(future_event_list, state, clock , customers)
            elif current_event['Event type'] == 'OF':
                OF(future_event_list, state, clock, current_event["Customer index"])
            elif current_event['Event type'] == 'RE':
                RE(future_event_list, state, clock, customers, current_event["Customer index"], )
            elif current_event['Event type'] == 'RF':
                RF(future_event_list, state, clock ,customers , current_event["Customer index"])
            elif current_event['Event type'] == 'SE':
                SE(future_event_list, state, clock, current_event["Customer index"])
            elif current_event['Event type'] == 'SF':
                SF(future_event_list, state, clock, current_event["Customer index"])
            elif current_event['Event type'] == 'E':
                E(clock , customers , current_event["Customer index"])
            elif current_event['Event type'] == 'OSRS':
                OSRS(future_event_list, state, clock)
            elif current_event['Event type'] == 'OSRF':
                OSRF(future_event_list, state, clock)
            elif current_event['Event type'] == 'RSRS':
                RSRS(future_event_list, state, clock)
            elif current_event['Event type'] == 'RSRF':
                RSRF(future_event_list, state, clock)

            #updating the cumulative statistics
            serving_food_queue_length.append(state['serving_queue'])
            ordering_queue_length.append(len(ordering_queue))
            receiving_queue_length.append(len(receiving_queue))
            
            #updating tracking table
            output_tracking_table = update(output_tracking_table, Real_clock, current_event, state, step)
            future_event_list.remove(current_event)
        else:
            break

    print("Restaurant is closed!")
    print("customer entering time to recieving")
    for i in range(len(customers)):
        print(customers[i].entering_time_to_receiving_section)
    print(total_time_customer_in_system)
    print(total_num_of_exited_customers)
    print(total_time_customer_in_receiving_queue)
    print(total_num_of_customers_received_food)
    print(total_ordering_server_busy_time)
    print(ordering_servers_rest_time)
    print(total_receiving_server_busy_time)
    print(receiving_servers_rest_time)
    
    print("mean time for customer being in the system")
    print(total_time_customer_in_system/total_num_of_exited_customers)
    print("mean customer's waiting time in receiving food")
    print(total_time_customer_in_receiving_queue/total_num_of_customers_received_food)
    print("mean of queue length in serving food part")
    print(sum(serving_food_queue_length)/len(serving_food_queue_length))
    print("maximum of queue length in serving food part")
    print(max(serving_food_queue_length))
    print("mean performance of the servers in ordering")
    print(total_ordering_server_busy_time/(5*simulation_time - ordering_servers_rest_time))
    print("mean performance of the servers in receiving")
    print(total_receiving_server_busy_time/(2*simulation_time - receiving_servers_rest_time))
    
    print(output_tracking_table)


simulation(int(input("Enter the Simulation Time: ")))
#print the outputs
