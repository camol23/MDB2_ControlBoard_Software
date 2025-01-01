'''
    Testing the sequence functions without GUI
'''


import matplotlib.pyplot as plt
import time

import HVbase_lib


number_chips =  2

device_hv513 = HVbase_lib.HV513()
device_hv513.clk_time = 0.001                                  # Clk signal semi-Period
device_hv513.time_LE = 0.001                                   # HV Outputs Update time



# Test one Electrode
point = 13
total_bits = 8*number_chips
output_binary = HVbase_lib.inverse_bit(point, total_bits)
print("Electrode position = ", point)
print("Input from inverse function = ", bin(output_binary))

device_hv513.num_chips = number_chips
device_hv513.send_data_debug(output_binary)
device_hv513.vis_send_debug()


# Testing Path 
points_list = [1, 4, 7, 13, 15] 
output_binary = HVbase_lib.map2_inverse_listPath(points_list, number_chips)
print("list of Electrodes positions = ", points_list)
print("Input from map function (last element)= ", bin(output_binary[-1]))

device_hv513.num_chips = number_chips
device_hv513.send_sequence_debug(output_binary)


# Testing Sequence
# Each step activates several electrodes
points_list = [[1, 3], [15, 0]] 
output_binary = HVbase_lib.map2_inverse_sequence(points_list, number_chips)
print("list of Electrodes positions = ", points_list)
print("Input from map function (last element)= ", bin(output_binary[-1]))

device_hv513.num_chips = number_chips
device_hv513.send_sequence_debug(output_binary)






