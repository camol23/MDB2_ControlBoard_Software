from Control_board import HVbase_lib
from Control_board import Board_GUI
import pygame
import sys

# points_list = [1, 5] 
# output_bi = HVbase_lib.map_from_path(points_list)
# print(bin(output_bi))



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
sys.exit()