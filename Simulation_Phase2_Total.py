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

print("Restaurant is closed!")




import random
import math
import pandas as pd
import numpy as np
from operator import itemgetter

#performance measures
performance_measures = dict()
performance_measures["mean time for customer being in the system"] = []
performance_measures["mean customer's waiting time in receiving food"] = []
performance_measures["mean of queue length in serving food part"] = []
performance_measures["maximum of queue length in serving food part"] = []
performance_measures["mean performance of the servers in ordering"] = []
performance_measures["mean performance of the servers in receiving"] = []
performance_measures["mean of queue length in ordering food part"] = []
performance_measures["mean of queue length in receiving food part"] = []


#system parameters
num_of_ordering_servers = 5
num_of_receiving_servers = 2
num_of_chairs_in_serving_food = 30
walking_mean_time = 0.5
exitting_mean_time = 1
ordering_parameters = {"min" : 1 , "mid" : 2 , "max" : 4}
payment_parameters = {"min" : 1 , "mid" : 2 , "max" : 3}
receiving_parameters = {"min" : 0.5 , "max" : 2}
serving_parameters = {"min" : 10 , "mid" : 20 , "max" : 30}
resting_time = 10
PCE_mean_arrival_time = 3
CCE_mean_arrival_time = 5
bus_mean_passangers = 30

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

    step = 0

    # State
    state = dict()
    state['Ordering_Server_Idle'] = num_of_ordering_servers
    state['Ordering_Server_Resting'] = 0
    state['Ordering_Server_Rest_blocked'] = 0
    state['Ordering_queue'] = 0
    state['Receiving_Server_Idle'] = num_of_receiving_servers
    state['Receiving_Server_Resting'] = 0
    state['Receiving_Server_Rest_blocked'] = 0
    state['Receiving_queue'] = 0
    state['Serving_Chairs_Idle'] = num_of_chairs_in_serving_food
    state['serving_queue'] = 0

    # the initial FEL
    future_event_list = list()
    FEL_maker(future_event_list, ["Event type" , "Event time" ],  ["PCE" , exponential_random_variate(PCE_mean_arrival_time)])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["CCE" , exponential_random_variate(CCE_mean_arrival_time)])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["BE" , random_uniform_between(60 , 180)])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 50])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 110])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 230])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["OSRS" , 290])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 50])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 110])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 230])
    FEL_maker(future_event_list, ["Event type" , "Event time" ] , ["RSRS" , 290])
    return state, future_event_list, step, clock


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
    FEL_maker(future_event_list, ["Event type" , "Event time"], ["PCE" , clock + exponential_random_variate(PCE_mean_arrival_time)])
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
        ordering = triangular_random_variate(ordering_parameters["min"],ordering_parameters["mid"], ordering_parameters["max"])
        paying_money = triangular_random_variate(payment_parameters["min"],payment_parameters["mid"], payment_parameters["max"])
        FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , customer_index])
        #updating the cumulative statistics
        global total_ordering_server_busy_time
        total_ordering_server_busy_time += ordering + paying_money

# Car Customer Enterance
# should be developed by Abolfazl
def CCE(future_event_list, state, clock, customers):
    #appending the next CCE event to the FEL
    FEL_maker(future_event_list, ["Event type" , "Event time"], ["CCE" , clock + exponential_random_variate(CCE_mean_arrival_time)])
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
            ordering = triangular_random_variate(ordering_parameters["min"],ordering_parameters["mid"], ordering_parameters["max"])
            paying_money = triangular_random_variate(payment_parameters["min"],payment_parameters["mid"], payment_parameters["max"])
            FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , customer_index])
            #updating the cumulative statistics
            global total_ordering_server_busy_time
            total_ordering_server_busy_time += ordering + paying_money



# Bus Entrance
# should be developed by Mohammad Sadegh
def BE(future_event_list, state, clock, customers):
    p = int(poisson_random_variate(bus_mean_passangers))
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
            ordering = triangular_random_variate(ordering_parameters["min"],ordering_parameters["mid"], ordering_parameters["max"])
            paying_money = triangular_random_variate(payment_parameters["min"],payment_parameters["mid"], payment_parameters["max"])
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
        FEL_maker(future_event_list, ["Event type", "Event time"], ["OSRF", clock + resting_time])
    going_to_receive = exponential_random_variate(walking_mean_time)
    FEL_maker(future_event_list, ["Event type", "Event time", "Customer index"],["RE", clock + going_to_receive, customer_index])
    if state["Ordering_queue"] == 0:
        if state["Ordering_Server_Idle"] < num_of_ordering_servers:
            state["Ordering_Server_Idle"] += 1
    else:
        state["Ordering_queue"] -= 1
        # random variates for determining time of ordering process and paying the money
        ordering = triangular_random_variate(ordering_parameters["min"],ordering_parameters["mid"], ordering_parameters["max"])
        paying_money = triangular_random_variate(payment_parameters["min"],payment_parameters["mid"], payment_parameters["max"])
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
        receiving = random_uniform_between(receiving_parameters["min"],receiving_parameters["max"])
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
    FEL_maker(future_event_list,["Event type" , "Event time" , "Customer index"], ["SE" , clock + exponential_random_variate(walking_mean_time) , customer_index])
    if state['Receiving_Server_Rest_blocked'] == 1 :
        state['Receiving_Server_Rest_blocked'] = 0
        state['Receiving_Server_Resting'] += 1
    if  state['Receiving_queue'] == 0 :
        if state['Receiving_Server_Idle'] < num_of_receiving_servers:
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
        serving = triangular_random_variate(serving_parameters["min"], serving_parameters["mid"], serving_parameters["max"])
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
        serving = triangular_random_variate(serving_parameters["min"], serving_parameters["mid"], serving_parameters["max"])
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
        FEL_maker(future_event_list, ["Event type", "Event time"], ["OSRF", clock + resting_time ])

# Ordering Server Rest Finish
# should be developed by Abolfazl
def OSRF(future_event_list, state, clock ):
    state['Ordering_Server_Resting'] = 0
    if state['Ordering_queue'] == 0:
        if state['Ordering_Server_Idle'] < num_of_ordering_servers:
            state['Ordering_Server_Idle'] += 1
    else:
        state['Ordering_queue'] -= 1
        #random variates for determining time of ordering process and paying the money
        ordering = triangular_random_variate(ordering_parameters["min"],ordering_parameters["mid"], ordering_parameters["max"])
        paying_money = triangular_random_variate(payment_parameters["min"],payment_parameters["mid"], payment_parameters["max"])
        #this should be completed when the OF event developed
        global ordering_queue
        FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["OF" , clock + ordering + paying_money , ordering_queue[0].index])
        ordering_queue.remove(ordering_queue[0])
        # updating the cumulative statistics
        global total_ordering_server_busy_time
        total_ordering_server_busy_time +=  ordering + paying_money
    #updating the cumulative statistics
    global ordering_servers_rest_time
    ordering_servers_rest_time += resting_time


# Receiving Server Rest Start
# should be developed by Abolfazl
def RSRS(future_event_list, state, clock):
    if state['Receiving_Server_Idle'] == 0:
        state['Receiving_Server_Rest_blocked'] += 1
    else:
        state['Receiving_Server_Resting'] += 1
        FEL_maker(future_event_list, ["Event type" , "Event time"], ["RSRF" , clock + resting_time])

# Receiving Server Rest Finish
# should be developed by Abolfazl
def RSRF(future_event_list, state, clock):
    state['Receiving_Server_Resting'] = 0
    if state['Receiving_queue'] == 0:
        if state['Receiving_Server_Idle'] < num_of_receiving_servers:
            state['Receiving_Server_Idle'] += 1
    else:
        state['Receiving_queue'] -= 1
        #random variates for determining time of receiving the ordered food
        receiving = random_uniform_between(receiving_parameters["min"] , receiving_parameters["max"])
        #this should be completed when the OF event developed
        global receiving_queue
        FEL_maker(future_event_list, ["Event type" , "Event time" , "Customer index"], ["RF" , clock + receiving , receiving_queue[0].index])
        receiving_queue.remove(receiving_queue[0])
    #updating the cumulative statistics
    global receiving_servers_rest_time
    receiving_servers_rest_time += resting_time


def update(output_tracking_table, clock, current_event, state, step):

    new_row = dict()
    new_row["step"] = step
    new_row["clock"] = clock
    new_row["hour"] = 10 + int(clock/60)
    new_row["minute"] = clock % 60
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
    new_row["ordering_servers_rest_time"] = ordering_servers_rest_time
    new_row["total_receiving_server_busy_time"] = total_receiving_server_busy_time
    new_row["receiving_servers_rest_time"] = receiving_servers_rest_time
    new_row["ordering_queue_length"] = ordering_queue_length[step-1]
    new_row["receiving_queue_length"] = ordering_queue_length[step-1]
    if total_num_of_exited_customers != 0 :
        new_row["mean time for customer being in the system"] = total_time_customer_in_system/total_num_of_exited_customers
    else :
         new_row["mean time for customer being in the system"] = "Null"
    if total_num_of_customers_received_food != 0:
        new_row["mean customer's waiting time in receiving food"] = total_time_customer_in_receiving_queue/total_num_of_customers_received_food
    else :
        new_row["mean customer's waiting time in receiving food"] = "Null"
    new_row["mean of queue length in serving food part"] = sum(serving_food_queue_length)/len(serving_food_queue_length)
    new_row["maximum of queue length in serving food part"] = max(serving_food_queue_length)
    if (num_of_ordering_servers*clock - ordering_servers_rest_time) != 0:
        new_row["mean performance of the servers in ordering"] = total_ordering_server_busy_time/(num_of_ordering_servers*clock - ordering_servers_rest_time)
    else :
        new_row["mean performance of the servers in ordering"] = "Null"
    if (num_of_receiving_servers*clock - receiving_servers_rest_time) != 0:
        new_row["mean performance of the servers in receiving"] = total_receiving_server_busy_time/(num_of_receiving_servers*clock - receiving_servers_rest_time)
    else :
        new_row["mean performance of the servers in ordering"] = "Null"
    if len(ordering_queue_length) != 0:
        new_row["mean of queue length in ordering food part"] = sum(ordering_queue_length)/len(ordering_queue_length)
    else :
        new_row["mean of queue length in ordering food part"] = "Null"
    if len(receiving_queue_length) != 0:
        new_row["mean of queue length in receiving food part"] = sum(receiving_queue_length)/len(receiving_queue_length)
    else :
        new_row["mean of queue length in receiving food part"] = "Null"


    #append row to the dataframe
    output_tracking_table = output_tracking_table.append(new_row, ignore_index=True)
    return output_tracking_table

def expot_data_frame_into_excel_with_adjustment(output_tracking_table):

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('R1.xlsx', engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    output_tracking_table.to_excel(writer, sheet_name='Sheet1' , startrow=1, header=False)
    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    # Add a header format
    #in the following link you can see the list of fg_color codes for 255 different color
    #https://plumbum.readthedocs.io/en/latest/colors.html
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'align': 'center', 'valign': 'vcenter', 'fg_color': '#A8A8A8','border': 1})
    # Write the column headers with the defined format
    for col_num, value in enumerate(output_tracking_table.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)
    # Add a header format
    cell_format = workbook.add_format({'bold': False,'text_wrap': True,'align': 'center', 'valign': 'vcenter','border': 1})
    # Set the format but not the column width.
    worksheet.set_column('B:ZZ', None , cell_format)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

# should be developed by Abolfazl
def simulation(simulation_time):
    output_tracking_table = pd.DataFrame(columns=["step" , "clock", "hour" , "minute" , "current event type", "Ordering_Server_Idle", "Ordering_Server_Resting" , "Ordering_Server_Rest_blocked",
    "Ordering_queue" , "Receiving_Server_Idle" , "Receiving_Server_Resting" , "Receiving_Server_Rest_blocked", "Receiving_queue" , "Serving_Chairs_Idle" ,
    "serving_queue" , "total_time_customer_in_system","total_num_of_exited_customers","total_time_customer_in_receiving_queue",
    "total_num_of_customers_received_food","serving_food_queue_length","total_ordering_server_busy_time", "ordering_servers_rest_time" , "total_receiving_server_busy_time" ,
    "receiving_servers_rest_time" , "ordering_queue_length" , "receiving_queue_length" , "mean time for customer being in the system",  "mean customer's waiting time in receiving food",
     "mean of queue length in serving food part" , "maximum of queue length in serving food part" , "mean performance of the servers in ordering" , "mean performance of the servers in receiving",
     "mean of queue length in ordering food part" , "mean of queue length in receiving food part" ])

    state, future_event_list , step, clock= starting_state()

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
        
        for i in range(len(customers)):
            print("customer" , customers[i].index)
            print(customers[i].entering_time_to_receiving_section)
        
        print(sorted_fel)
        """
        step += 1
        current_event = sorted_fel[0]
        clock = current_event['Event time']

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
            output_tracking_table = update(output_tracking_table, clock, current_event, state, step)
            future_event_list.remove(current_event)
        else:
            break

    print("Restaurant is closed!")
    print("mean time for customer being in the system")
    print(total_time_customer_in_system/total_num_of_exited_customers)
    print("mean customer's waiting time in receiving food")
    print(total_time_customer_in_receiving_queue/total_num_of_customers_received_food)
    print("mean of queue length in serving food part")
    print(sum(serving_food_queue_length)/len(serving_food_queue_length))
    print("maximum of queue length in serving food part")
    print(max(serving_food_queue_length))
    print("mean performance of the servers in ordering")
    print(total_ordering_server_busy_time/(num_of_ordering_servers*simulation_time - ordering_servers_rest_time))
    print("mean performance of the servers in receiving")
    print(total_receiving_server_busy_time/(num_of_receiving_servers*simulation_time - receiving_servers_rest_time))
    print("mean of queue length in ordering food part")
    print(sum(ordering_queue_length)/len(ordering_queue_length))
    print("mean of queue length in receiving food part")
    print(sum(receiving_queue_length)/len(receiving_queue_length))

    performance_measures["mean time for customer being in the system"].append(total_time_customer_in_system/total_num_of_exited_customers)
    performance_measures["mean customer's waiting time in receiving food"].append(total_time_customer_in_receiving_queue/total_num_of_customers_received_food)
    performance_measures["mean of queue length in serving food part"].append(sum(serving_food_queue_length)/len(serving_food_queue_length))
    performance_measures["maximum of queue length in serving food part"].append(max(serving_food_queue_length))
    performance_measures["mean performance of the servers in ordering"].append(total_ordering_server_busy_time/(num_of_ordering_servers*simulation_time - ordering_servers_rest_time))
    performance_measures["mean performance of the servers in receiving"].append(total_receiving_server_busy_time/(num_of_receiving_servers*simulation_time - receiving_servers_rest_time))
    performance_measures["mean of queue length in ordering food part"].append(sum(ordering_queue_length)/len(ordering_queue_length))
    performance_measures["mean of queue length in receiving food part"].append(sum(receiving_queue_length)/len(receiving_queue_length))
    expot_data_frame_into_excel_with_adjustment(output_tracking_table)


replications = int(input("Enter the number of replications: "))
simulation_time = int(input("Enter the Simulation Time: "))
for i in range(replications):
    print("--------------- replication " , i+1 ," ---------------")
    simulation(simulation_time)

#print the outputs which are averages of performance measures in specified replication numbers
print("average of " , replications , " replications for mean time for customer being in the system")
print(sum(performance_measures["mean time for customer being in the system"])/len(performance_measures["mean time for customer being in the system"]))
print("average of " , replications , " replications for mean customer's waiting time in receiving food")
print(sum(performance_measures["mean customer's waiting time in receiving food"])/len(performance_measures["mean customer's waiting time in receiving food"]))
print("average of " , replications , " replications for mean of queue length in serving food part")
print(sum(performance_measures["mean of queue length in serving food part"])/len(performance_measures["mean of queue length in serving food part"]))
print("average of " , replications , " replications for maximum of queue length in serving food part")
print(sum(performance_measures["maximum of queue length in serving food part"])/len(performance_measures["maximum of queue length in serving food part"]))
print("average of " , replications , " replications for mean performance of the servers in ordering")
print(sum(performance_measures["mean performance of the servers in ordering"])/len(performance_measures["mean performance of the servers in ordering"]))
print("average of " , replications , " replications for mean performance of the servers in receiving")
print(sum(performance_measures["mean performance of the servers in receiving"])/len(performance_measures["mean performance of the servers in receiving"]))
print("average of " , replications , " replications for mean of queue length in ordering food part")
print(sum(performance_measures["mean of queue length in ordering food part"])/len(performance_measures["mean of queue length in ordering food part"]))
print("average of " , replications , " replications for mean time for customer being in the system")
print(sum(performance_measures["mean of queue length in receiving food part"])/len(performance_measures["mean of queue length in receiving food part"]))
