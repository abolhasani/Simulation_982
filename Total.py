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
    #FEL_maker(future_event_list,  ,  )

    return state, future_event_list, step, clock, Real_clock


# a function for making new event notices and adding them to the FEL
def FEL_maker(future_event_list,keys, values):
    new_event = dict()
    for i in range(len(keys)):
        new_event[keys[i]] = values[i]
    future_event_list.append(new_event)
