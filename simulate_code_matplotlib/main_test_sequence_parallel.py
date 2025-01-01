'''
    Testing the sequence functions without GUI
'''


import matplotlib.pyplot as plt
import time

from Control_board import HVbase_lib



device_hv513 = HVbase_lib.HV513()
device_hv513.clk_time = 0.001                                  # Clk signal semi-Period
device_hv513.time_LE = 0.001                                   # HV Outputs Update time


virtual = []
# Testing Path 
points_list = [1, 4, 7, 13, 15, 16, 31] 
output_binary = HVbase_lib.map_from_parallel_path(points_list)
print("list of Electrodes positions = ", points_list)
print("Input from map function (last element)= ")
for bin_val in output_binary:
    print(bin(bin_val))

virtual.append(output_binary)
device_hv513.send_sequence_parallel_debug(virtual)        # Works


# Testing Sequence
# Each step activates several electrodes
points_list = [[1, 3], [15, 0]] 
output_binary = HVbase_lib.map_from_parallel_sequence(points_list)
print("list of Electrodes positions = ", points_list)
print("Input from map function (last element)= ")
for i, bin_list in enumerate(output_binary):
    print("Sequence #", i)
    for bin_val in bin_list:
        print(bin(bin_val))


device_hv513.send_sequence_parallel_debug(output_binary)






