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
# Close and End
pygame.quit()



# points_list = [1, 4, 7, 12, 15] s
output_binary = HVbase_lib.map_from_path(board.path_list)
print("list of Electrodes positions = ", board.path_list)
print("Input from map function = ", bin(output_binary))

device_hv513.num_chips = 2
device_hv513.send_data_debug(output_binary)
device_hv513.vis_send_debug()




print("...... ENDED .......")
sys.exit()
