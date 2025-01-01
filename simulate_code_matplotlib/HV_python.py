import matplotlib.pyplot as plt
import time

import HVbase_lib


device_hv513 = HVbase_lib.HV513()
device_hv513.clk_time = 0.001                                  # Clk signal semi-Period


data_to_send = 0b0101_0101
device_hv513.send_data_debug(data_to_send)
device_hv513.vis_send_debug()


# data_to_send = 0b0101_0101_0101_0101 
# device_hv513.num_chips = 2
# device_hv513.send_data_debug(data_to_send)
# device_hv513.vis_send_debug()

points_list = [1, 4, 7, 12, 15] 
output_binary = HVbase_lib.map_from_path(points_list)
print("list of Electrodes positions = ", points_list)
print("Input from map function = ", bin(output_binary))

device_hv513.num_chips = 2
device_hv513.send_data_debug(output_binary)
device_hv513.vis_send_debug()


points_list = [1,3] 
output_binary = HVbase_lib.map_from_path(points_list)
print("list of Electrodes positions = ", points_list)
print("Input from map function = ", bin(output_binary))

device_hv513.num_chips = 2
device_hv513.send_data_debug(output_binary)
device_hv513.vis_send_debug()


# data_to_send = 0b0111_0111
# device_hv513.num_chips = 1
# device_hv513.send_data_debug(data_to_send)
# device_hv513.vis_send_debug()



