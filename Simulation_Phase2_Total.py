"""
Simulation of fast-food restaurant
system description should be added
Outputs : 1-mean time for customer being in the system
          2-mean customer's waiting time in receiving food
          3-mean and maximum of queue length in serving food part
          4-mean performance of the servers in ordering and receiving part
          5-mean number of customers in the system
Starting State = ...

Authors: Mohammad Sadegh Abolhasani, Abolfazl Tghavi
Starting Date:9 May 2020
Finishing Date:... May 2020
"""

import random
import math
import pandas as pd
###import numpy as np
from operator import itemgetter


# an array for holding the information of all customers attended
customers = []
# defining statistics which should be updated during the simulation
total_time_customer_in_system = 0
total_num_of_exited_customers = 0
total_time_customer_in_receiving_queue = 0
total_num_of_customers_received_food = 0
serving_food_queue_length = []
total_ordering_server_busy_time = 0
total_receiving_server_busy_time = 0
ordering_servers_rest_time = 0
receiving_servers_rest_time = 0


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
    FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["PCE" , exponential_random_variate(3) , 0])

    return state, future_event_list, step, clock, Real_clock


# a function for making new event notices and adding them to the FEL
def FEL_maker(future_event_list,keys, values):
    new_event = dict()
    for i in range(len(keys)):
        new_event[keys[i]] = values[i]
    future_event_list.append(new_event)

# should be developed by Abolfazl
def triangular_random_variate(a , b , c , R):
    def triangular_random_variate(a, b, c , R):
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
    return 0


# should be developed by Abolfazl
def num_of_car_passangers(R):
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

# Pedestrian Customer Entrance
# should be developed by Abolfazl
def PCE(future_event_list, state, clock , customers):
    customer_index = len(customers)
    #appending the next PCE event to the FEL
    FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["PCE" , clock + exponential_random_variate(3) , customer_index])
    #instantiating a new customer and appendign it to the list of customers
    customer = Customer(customer_index, clock)
    customers.append(customer)

    if state["Ordering_Server_Idle"] == 0:
        state["Ordering_queue"] += 1
    else :
        state["Ordering_Server_Idle"] -= 1
        #random variates for determining time of ordering process and paying the money
        ordering = triangular_random_variate(1, 2, 4 , np.random.random())
        paying_money = triangular_random_variate(1, 2, 3)
        #this should be completed when the OF event developed
        FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , customer_index])
    #updating the cumulative statistics
    #there is no need to update the cumulative statistics here

# Car Customer Enterance
# should be developed by Abolfazl
def CCE(future_event_list, state, clock ,customers):
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
        else :
            state["Ordering_Server_Idle"] -= 1
            #random variates for determining time of ordering process and paying the money
            ordering = triangular_random_variate(1, 2, 4)
            paying_money = triangular_random_variate(1, 2, 3)
            #this should be completed when the OF event developed
            FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , customer_index])
        #updating the cumulative statistics
        #there is no need to update the cumulative statistics here
          
 # Bus Entrance
# should be developed by Mohammad Sadegh
def BE(future_event_list, state, clock, total_ordering_server_busy_time):
    p = int(poisson_random_variate(30))
    #clock = (random_uniform_between(11,13) - 11 )* 60
    for i in range(p):
        customer_index = len(customers)
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],
                  ["OE", clock, customer_index])
        # instantiating a new customer and appending it to the list of customers
        customer = Customer(customer_index, clock)
        customers.append(customer)
        if state["Ordering_Server_Idle"] == 0:
            state["Ordering_queue"] += 1
        else:
            state["Ordering_Server_Idle"] -= 1
            # random variates for determining time of ordering process and paying the money
            ordering = triangular_random_variate(1, 2, 4)
            paying_money = triangular_random_variate(1, 2, 3)
            # this should be completed when the OF event developed
            FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],
                      ["OF", clock + ordering + paying_money, customer_index])
            total_ordering_server_busy_time +=  ordering + paying_money
        # updating the cumulative statistics
        # there is no need to update the cumulative statistics here


# Ordering Finish
# should be developed by Mohammad Sadegh
def OF(future_event_list, state, clock, customers, customer_index, ordering_servers_rest_time, total_ordering_server_busy_time):
    if state["Ordering_Server_Rest_blocked"] == 1:
        state["Ordering_Server_Rest_blocked"] = 0
        state['Ordering_Server_Resting'] += 1
        ordering_servers_rest_time +=  10
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],
                  ["OSRF", clock + 10, customers[customer_index]])
    going_to_receive = exponential_random_variate(0.5)
    FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],
              ["RE", clock + going_to_receive, customers[customer_index]])
    if state["Ordering_queue"] == 0:
        state["Ordering_server_idle"] += 1
    else:
        state["Ordering_queue"] -= 1
        # random variates for determining time of ordering process and paying the money
        ordering = triangular_random_variate(1, 2, 4)
        paying_money = triangular_random_variate(1, 2, 3)
        # this should be completed when the OF event developed
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],
                  ["OF", clock + ordering + paying_money, customers[customer_index]])
        total_ordering_server_busy_time += ordering + paying_money
    # updating the cumulative statistics
    # there is no need to update the cumulative statistics here


# Receiving Entrance
# should be developed by Mohammad Sadegh
def RE(future_event_list, state, clock, customers, customer_index, total_time_customer_in_receiving_queue, total_receiving_server_busy_time):
    if state["Receiving_Server_Idle"] == 0:
        state["Receiving_queue"] += 1
        #total_time_customer_in_receiving_queue += clock - customers[customer_index].entering_receiving_section_time
    else:
        state["Receiving_Server_Idle"] -= 1
        # random variates for determining time of ordering process and paying the money
        receiving = random_uniform_between(0.5,2)
        # this should be completed when the OF event developed
        FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],
                  ["RF", clock + receiving, customers[customer_index]])
        customers[customer_index].entering_receiving_section_time = clock
        total_receiving_server_busy_time += receiving
    # updating the cumulative statistics
    # there is no need to update the cumulative statistics here

# Receiving Finish
# should be developed by Abolfazl
def RF(future_event_list, state, clock , total_time_customer_in_receiving_queue , total_num_of_customers_received_food , customers , customer_index):
    #this part should be completed after abol's part
    FEL_maker(future_event_list,["Event type" , "Event time"], ["SE" , clock + exponential_random_variate(0.5)])
    if state['Receiving_Server_Rest_blocked'] == 1 :
        state['Receiving_Server_Rest_blocked'] = 0
        state['Receiving_Server_Resting'] += 1
    if  state['Receiving_queue'] == 0 :
        state['Receiving_Server_Idle'] += 1
        state['Receiving_queue'] -= 1
        FEL_maker(future_event_list,["Event type" , "Event time" , "Customer index"], ["RF" , clock + random_uniform_between(0.5,2) , customer_index+1])

    #updating the cumulative statistics
    total_time_customer_in_receiving_queue += (clock - customers[customer_index].entering_time_to_receiving_section)
    total_num_of_customers_received_food += 1


