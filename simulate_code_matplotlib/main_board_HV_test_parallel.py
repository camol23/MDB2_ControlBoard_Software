from Control_board import HVbase_lib
from Control_board import Board_GUI

import pygame
import sys
import matplotlib.pyplot as plt
import time



device_hv513 = HVbase_lib.HV513()


# Hyper parameters
MAP_DIMENSIONS = (1200, 600)
map_env = '/home/camilo/Documents/SDU/SDU_courses/Third/MDB2/test_code/HV_converter/testing_python/Images/blank_background.png'

board = Board_GUI.Graphics(MAP_DIMENSIONS, map_img_path=map_env)



# Display
running = True

while running:

    running = board.dectect_actions()

    board.draw_board()
    pygame.display.update()


print("The selected electrodes are =  ", board.path_list)
points_list = board.path_list
# Close and End
pygame.quit()



# points_list = [1, 4, 7, 12, 15] 
virtual =[]
if board.group_flag:
    output_binary = HVbase_lib.map_from_parallel_sequence(points_list)
else:
    output_binary = HVbase_lib.map_from_parallel_path(points_list)
print("list of Electrodes positions = ", points_list)
print("Input from map function (last element)= ")

if board.group_flag:
    virtual = output_binary.copy()
    for i, bin_list in enumerate(output_binary):
        print("Sequence #", i)
        for bin_val in bin_list:
            print(bin(bin_val))
else:
    virtual.append(output_binary)
    for bin_val in output_binary:
        print(bin(bin_val))

device_hv513.send_sequence_parallel_debug(virtual)        # Works




print("...... ENDED .......")
sys.exit()
