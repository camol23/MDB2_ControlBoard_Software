'''
    HV513 Datasheet
    https://ww1.microchip.com/downloads/en/DeviceDoc/HV513-8-Channel-Serial-to-Parallel-Converter-with-High-Voltage-Push-Pull-Outputs-Polarity-Hi-Z-and-Short-Circuit-Detect-Data-Sheet.pdf

'''

# import RPi.GPIO as GPIO
import time

# Just for Debug function 
import matplotlib.pyplot as plt
import numpy as np



class HV513():
    def __init__(self, num_chips = 1, sending_time_LE = 0.001):
        ''' 
            Update:
                1) GPIO Pins
        
        '''
        
        # HV513 GPIO Pins
        self.BL = 4                 # Blank val         (0: Set Low HV - [~BL NAND Latch_Output] )
        self.POL = 5                # Polarity val      (1: exact in and out val - [~POL XOR Latch_Output])
        self.HI_Z = 6               # High Impedance    (0: Set high Z in the OUput)

        self.CLK = 1                # Clock signal      (rise-up to shift data input)
        self.LE = 2                 # Latch enable      (1: Load D_in to D_out)
        self.DATA = 3               # Data to be sended to D_in (1-bit serial Output)
        self.DATA2 = 7              # D_in 2 for the second HV
        self.DATA3 = 8              # D_in 3 for the third HV
        self.DATA4 = 9              # D_in 4 for the fourth HV

        # HV513 Sginals
        self.BL_val = 0b1               # Blank val         (0: Set Low HV - [~BL NAND Latch_Output] )
        self.POL_val = 0b1              # Polarity val      (1: exact in and out val - [~POL XOR Latch_Output])
        self.HI_Z_val = 0b1             # High Impedance    (0: Set high Z in the OUput)

        self.CLK_val = 0b0              # Clock signal      (rise-up to shift data input)
        self.LE_val = 0b0               # Latch enable      (1: Load D_in to D_out)
        # self.DATA_val = 0b0000_0000   # Data to be sended to D_in (8-bits Output one chip)

        # Settings vals
        self.clk_time = 0.001           # Clk signal semi-Period
        self.time_LE = sending_time_LE  # HV Outputs Update time
        self.num_chips = num_chips      # Number of chips connected in cascaded ( D_out feed D_in(next) )    


        # Init
        self.setup()
        self.reset()


        # Debuging arrays
        self.DATA_val = 0b0                 # Data to be sended to D_in 
        self.CLK_list = [self.CLK_val]              
        self.LE_list = [self.LE_val]               
        self.DATA_list = [self.DATA_val]
        self.data_in = 0

        self.DATA2_val = 0b0                 
        self.DATA2_list = [self.DATA2_val]
        self.DATA3_val = 0b0                 
        self.DATA3_list = [self.DATA3_val]
        self.DATA4_val = 0b0                 
        self.DATA4_list = [self.DATA4_val]
        self.data_in_list = []



    def send_sequence(self, data_list):
        '''
            Send a sequence of electrodes to be activated which defines a path in the Board
            
                Note:
                        1) Data_list should came from (map2) functions 
                        2) Should be define time_LE to establish the sequence time 

        '''
        for data in data_list:
            self.send_data(data)

            time.sleep(self.time_LE)



    def send_data(self, data_in):
        '''
            Send data from the LS-Bit to the MS-Bit of Data_in

                Note: the LS-Bit Data_in is goint to be related
                      with the first pin in the HV513 (HVOUT1)
        '''
        self.reset()
        
        for j in range(0, self.num_chips):
            for i in range(0, 8):                           # Each chip manage 8-bit Input
                data_bit = data_in & 1                      # Take the first bit
                self.set_GPIO(self.DATA, data_bit)           # Load bit to the GPIO DATA
                
                self.CLK_val = 0b1 
                self.set_GPIO(self.CLK, self.CLK_val)       # Load bit to the GPIO CLK 
                data_in = data_in >> 1                      # shift data to be serialized
                
                time.sleep(self.clk_time)                   # Positive clk semi-cycle                 
                self.CLK_val = 0b0
                self.set_GPIO(self.CLK, self.CLK_val)       # Load bit to the GPIO CLK 
                time.sleep(self.clk_time)                   # Positive clk semi-cycle

        self.LE_val = 0b1
        self.set_GPIO(self.LE, self.LE_val)             # Load bit to the GPIO LE

        time.sleep(self.clk_time)
        self.LE_val = 0b0
        self.set_GPIO(self.LE, self.LE_val)             # Load bit to the GPIO LE

    
    def reset(self):
        self.CLK_val = 0b0
        self.LE_val = 0b0
        data_in = 0b0

        self.BL_val = 0b1
        self.POL_val = 0b1       
        self.HI_Z_val = 0b1  

        self.set_GPIO(self.DATA, data_in)
        self.set_GPIO(self.CLK, self.CLK_val)
        self.set_GPIO(self.BL, self.BL_val)
        self.set_GPIO(self.POL, self.POL_val)
        self.set_GPIO(self.HI_Z, self.HI_Z_val)

    def deactivate(self):
        '''
            All off Sequence from Datasheet
            *) Result: All High-Voltage outputs (L)
        '''
        self.CLK_val = 0b0
        self.LE_val = 0b0
        data_in = 0b0

        self.BL_val = 0b0
        self.POL_val = 0b1       
        self.HI_Z_val = 0b1  

        self.set_GPIO(self.DATA, data_in)
        self.set_GPIO(self.CLK, self.CLK_val)
        self.set_GPIO(self.BL, self.BL_val)
        self.set_GPIO(self.POL, self.POL_val)
        self.set_GPIO(self.HI_Z, self.HI_Z_val)

    
    def setup(self):
        pass
        # GPIO.setmode(GPIO.BCM) # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(self.DATA, GPIO.OUT)
        # GPIO.setup(self.CLK, GPIO.OUT)
        # GPIO.setup(self.BL, GPIO.OUT)
        # GPIO.setup(self.POL, GPIO.OUT)
        # GPIO.setup(self.HI_Z, GPIO.OUT)

        # self.deactivate()



    def set_GPIO(self, pin, val):
        
        if (val & 1):
            pass
            # GPIO.output(pin, GPIO.HIGH)
        else:
            pass
            # GPIO.output(pin, GPIO.LOW)


    def blink(self):
        ''' 
            Testing if it is possible make a AC signal 
            switching BL or POL signals
        
        '''
        pass
    

    def send_sequence_debug(self, data_list):
        '''
            Send a sequence of electrodes to be activated which defines a path in the Board

            
                Note:
                        1) Data_list should came from (map2) functions 
                        2) Should be define time_LE to establish the sequence time 

        '''
        for data in data_list:
            self.send_data_debug(data)

            time.sleep(self.time_LE)
            self.vis_send_debug()


    def send_sequence_parallel_debug(self, data_list):

        for data in data_list:
            self.send_data_parallel_debug(data)

            time.sleep(self.time_LE)
            self.vis_send_parallel_debug()        


    def send_data_parallel_debug(self, data_in):
        '''
            data_in a list of 4 elements
            Each element represent one HV518
        '''

        # Include turn-on signals-funtion

        self.reset_stored_signals()

        self.CLK_val = 0b0
        self.LE_val = 0b0
        self.DATA_val = 0b0
        self.CLK_list = [self.CLK_val]              
        self.LE_list = [self.LE_val]               
        self.DATA_list = [self.DATA_val]
        
        # self.data_in = data_in
        self.data_in_list = [data_in[0], data_in[1], data_in[2], data_in[3]]
        
        self.DATA2_val = 0b0                 
        self.DATA2_list = [self.DATA2_val]
        self.DATA3_val = 0b0                 
        self.DATA3_list = [self.DATA3_val]
        self.DATA4_val = 0b0                 
        self.DATA4_list = [self.DATA4_val]

        data1_in = data_in[0]
        data2_in = data_in[1]
        data3_in = data_in[2]
        data4_in = data_in[3]
            
        for i in range(0, 8):                              # Each chip manage 8-bit Input
            # data_bit = data_in & 1                       # Take the first bit
            self.DATA_val = data1_in & 1
            self.store_signals_parallel(self.DATA, self.DATA_val)   # Load bit to the GPIO DATA
            self.DATA2_val = data2_in & 1
            self.store_signals_parallel(self.DATA2, self.DATA2_val)   # Load bit to the GPIO DATA
            self.DATA3_val = data3_in & 1
            self.store_signals_parallel(self.DATA3, self.DATA3_val)   # Load bit to the GPIO DATA
            self.DATA4_val = data4_in & 1
            self.store_signals_parallel(self.DATA4, self.DATA4_val)   # Load bit to the GPIO DATA
            
            self.CLK_val = 0b1 
            self.store_signals_parallel(self.CLK, self.CLK_val)      # Load bit to the GPIO CLK 
            data1_in = data1_in >> 1                          # shift data to be serialized
            data2_in = data2_in >> 1
            data3_in = data3_in >> 1
            data4_in = data4_in >> 1
            
            time.sleep(self.clk_time)                                  # Positive clk semi-cycle                 
            self.CLK_val = 0b0
            self.store_signals_parallel(self.CLK, self.CLK_val)        # Load bit to the GPIO CLK 
            time.sleep(self.clk_time)                                  # Positive clk semi-cycle
        

        self.LE_val = 0b1
        self.store_signals_parallel(self.LE, self.LE_val)                # Load bit to the GPIO LE

        time.sleep(self.clk_time)
        self.LE_val = 0b0
        self.store_signals_parallel(self.LE, self.LE_val)                # Load bit to the GPIO LE


    def send_data_debug(self, data_in):

        self.reset_stored_signals()

        self.CLK_val = 0b0
        self.LE_val = 0b0
        self.DATA_val = 0b0
        self.CLK_list = [self.CLK_val]              
        self.LE_list = [self.LE_val]               
        self.DATA_list = [self.DATA_val]
        self.data_in = data_in
        
        data_bit = 0b0

        # Verify num. bits and truncate them
        # ---- ToDo (not necessary)
        
        for j in range(0, self.num_chips):
            
            for i in range(0, 8):                              # Each chip manage 8-bit Input
                # data_bit = data_in & 1                       # Take the first bit
                self.DATA_val = data_in & 1
                self.store_signals(self.DATA, self.DATA_val)   # Load bit to the GPIO DATA
                
                self.CLK_val = 0b1 
                self.store_signals(self.CLK, self.CLK_val)      # Load bit to the GPIO CLK 
                data_in = data_in >> 1                          # shift data to be serialized
                
                time.sleep(self.clk_time)                       # Positive clk semi-cycle                 
                self.CLK_val = 0b0
                self.store_signals(self.CLK, self.CLK_val)      # Load bit to the GPIO CLK 
                time.sleep(self.clk_time)                       # Positive clk semi-cycle
        

        self.LE_val = 0b1
        self.store_signals(self.LE, self.LE_val)                # Load bit to the GPIO LE

        time.sleep(self.clk_time)
        self.LE_val = 0b0
        self.store_signals(self.LE, self.LE_val)                # Load bit to the GPIO LE


    def reset_stored_signals(self):
        self.DATA_list.clear()
        self.CLK_list.clear()
        self.LE_list.clear()

        self.DATA2_list.clear()
        self.DATA3_list.clear()
        self.DATA4_list.clear()

    def store_signals(self, pin, bit_val):
        
        if pin == self.DATA :
            self.DATA_list.append(bit_val)
            self.CLK_list.append(self.CLK_val)
            self.LE_list.append(self.LE_val)

            self.DATA_list.append(bit_val)
            self.CLK_list.append(self.CLK_val)
            self.LE_list.append(self.LE_val)
        
        if pin == self.CLK :
            self.DATA_list.append(self.DATA_val)
            self.CLK_list.append(bit_val)
            self.LE_list.append(self.LE_val)

            self.DATA_list.append(self.DATA_val)
            self.CLK_list.append(bit_val)
            self.LE_list.append(self.LE_val)
        
        if pin == self.LE :
            self.DATA_list.append(self.DATA_val)
            self.CLK_list.append(self.CLK_val)
            self.LE_list.append(bit_val)

            self.DATA_list.append(self.DATA_val)
            self.CLK_list.append(self.CLK_val)
            self.LE_list.append(bit_val)

    def store_signals_parallel(self, pin, bit_val):
        
        if pin == self.DATA :
            for _ in range(0,2):
                self.DATA_list.append(bit_val)
                self.DATA2_list.append(self.DATA2_val)
                self.DATA3_list.append(self.DATA3_val)
                self.DATA4_list.append(self.DATA4_val)
                
                self.CLK_list.append(self.CLK_val)
                self.LE_list.append(self.LE_val)

        if pin == self.DATA2 :
            for _ in range(0,2):
                self.DATA_list.append(self.DATA_val)
                self.DATA2_list.append(bit_val)
                self.DATA3_list.append(self.DATA3_val)
                self.DATA4_list.append(self.DATA4_val)
                
                self.CLK_list.append(self.CLK_val)
                self.LE_list.append(self.LE_val)

        if pin == self.DATA3 :
            for _ in range(0,2):
                self.DATA_list.append(self.DATA_val)
                self.DATA2_list.append(self.DATA2_val)
                self.DATA3_list.append(bit_val)
                self.DATA4_list.append(self.DATA4_val)
                
                self.CLK_list.append(self.CLK_val)
                self.LE_list.append(self.LE_val)

        if pin == self.DATA4 :
            for _ in range(0,2):
                self.DATA_list.append(self.DATA_val)
                self.DATA2_list.append(self.DATA2_val)
                self.DATA3_list.append(self.DATA3_val)
                self.DATA4_list.append(bit_val)
                
                self.CLK_list.append(self.CLK_val)
                self.LE_list.append(self.LE_val)

        
        if pin == self.CLK :
            for _ in range(0,2):
                self.DATA_list.append(self.DATA_val)
                self.DATA2_list.append(self.DATA2_val)
                self.DATA3_list.append(self.DATA3_val)
                self.DATA4_list.append(self.DATA4_val)
                
                self.CLK_list.append(bit_val)
                self.LE_list.append(self.LE_val)
        
        if pin == self.LE :
            for _ in range(0,2):
                self.DATA_list.append(bit_val)
                self.DATA2_list.append(self.DATA2_val)
                self.DATA3_list.append(self.DATA3_val)
                self.DATA4_list.append(self.DATA4_val)
                
                self.CLK_list.append(self.CLK_val)
                self.LE_list.append(bit_val)


    def vis_send_debug(self):
        t_list = np.arange(len(self.DATA_list))

        plt.plot(t_list, self.CLK_list, t_list, self.DATA_list, t_list, self.LE_list)
        plt.legend(['CLK', 'DATA', 'LE'])
        plt.title("Number of chips = " + str(self.num_chips) + " - Input Data = " + str(bin(self.data_in)))
        plt.show() 


    def vis_send_parallel_debug(self):
        
        t_list = np.arange(len(self.DATA_list))
        list_data = [self.DATA_list, self.DATA2_list, self.DATA3_list, self.DATA4_list]
        # for i in range(1, 5):
            
        #     data = list_data[i-1]

        #     plt.plot(t_list, self.CLK_list, t_list, data, t_list, self.LE_list)
        #     plt.legend(['CLK', 'DATA', 'LE'])
        #     plt.title("HV518 # " + str(i) + " - Input Data = " + str(bin(self.data_in_list[i-1])))
        #     plt.show() 
        data = list_data[0]
        plt.figure()
        plt.plot(t_list, self.CLK_list, t_list, data, t_list, self.LE_list)
        plt.legend(['CLK', 'DATA', 'LE'])
        plt.title("HV518 # " + str(1) + " - Input Data = " + str(bin(self.data_in_list[0])))

        data = list_data[1]
        plt.figure()
        plt.plot(t_list, self.CLK_list, t_list, data, t_list, self.LE_list)
        plt.legend(['CLK', 'DATA', 'LE'])
        plt.title("HV518 # " + str(2) + " - Input Data = " + str(bin(self.data_in_list[1])))

        data = list_data[2]
        plt.figure()
        plt.plot(t_list, self.CLK_list, t_list, data, t_list, self.LE_list)
        plt.legend(['CLK', 'DATA', 'LE'])
        plt.title("HV518 # " + str(3) + " - Input Data = " + str(bin(self.data_in_list[2])))

        data = list_data[3]
        plt.figure()
        plt.plot(t_list, self.CLK_list, t_list, data, t_list, self.LE_list)
        plt.legend(['CLK', 'DATA', 'LE'])
        plt.title("HV518 # " + str(4) + " - Input Data = " + str(bin(self.data_in_list[3])))

        plt.show()


# Global Package functions


def map_from_path(points_list):
    '''
        Transform the the electrodoce path to be activated 
        in a bit sequence to manage the HV513 array

        Input:
            1) points_list: Index (i.e. Electrode position or Id)
            2) num_elemets: The number of HV513s

        Note:
            1) The phisical arrangesment should follows:
                a) It's consider the HV513 outputs are the columns
                b) The HV513 are stack as rows
    '''
    
    # 32-bits := 4 HV513
    output_bin = 0b0000_0000_0000_0000_0000_0000_0000_0000
    base_bib = 0b0000_0000_0000_0000_0000_0000_0000_0001
    
    for idx in points_list:
        output_bin = output_bin | (base_bib << idx)

    return output_bin

def map_from_parallel_path(points_list):

    base_bin = 0b01
    output_bin = [0, 0, 0, 0]
    
    for idx in points_list:

        if idx <= 7 :
            i = 0
            id = idx
        elif idx <= 15 :
            i = 1
            id = idx - 8
        elif idx <= 23 :
            i = 2
            id = idx - 16
        elif idx <= 31 :
            i = 3
            id = idx - 24

        output_bin[i] = output_bin[i] | (base_bin << id)

    return output_bin

def map_from_parallel_sequence(points_list):

    output_sequence = []

    for points in points_list:
        output = map_from_parallel_path(points)
        output_sequence.append(output)

    return output_sequence


def map2_inverse_listPath(points_list, num_chips=4):
    '''
        Transform the the electrodes path to be activated 
        in a bit sequence to manage the HV513 array

            * Inverse the bits order (LSB turns to)

        Input:
            1) points_list: Index (i.e. Electrode position or Id)
            2) num_chips: The number of HV513s

        output:
            1) output_bin: list with sequence to activated the HV513 arragement

        Note:
            1) The phisical arrangesment should follows:
                a) It's consider the HV513 outputs are the columns
                b) The HV513 are stack as rows
    '''
    
    # 32-bits := 4 HV513
    output_list = []

    total_bits =  num_chips*8
    for idx in points_list:
        bin_val = inverse_bit(idx, total_bits)
        output_list.append(bin_val)

    return output_list


def map2_inverse_sequence(points_list, num_chips=4):
    '''
        Transform the group of electrodes to be activated 
        in a bit sequence to manage the HV513 array

            * Inverse the bits order (LSB turns to)

        Input:
            1) points_list: *) It should be a list of lists, 
                            where inner list represent 
                            the electrodes actived at the same time
                            *) Index (i.e. Electrode position or Id)

            2) num_chips: The number of HV513s

        output:
            1) output_bin: list with sequence to activated the HV513 arragement

        Note:
            1) The phisical arrangesment should follows:
                a) It's consider the HV513 outputs are the columns
                b) The HV513 are stack as rows
    '''
    
    # 32-bits := 4 HV513
    output_bin = 0b0000_0000_0000_0000_0000_0000_0000_0000
    output_list = []

    total_bits =  num_chips*8
    for i in range(0, len(points_list)):

        for idx in points_list[i]:
            bin_val = inverse_bit(idx, total_bits)
            output_bin = output_bin | bin_val

        output_list.append(output_bin)
        output_bin = 0

    return output_list


def inverse_bit(idx, total_bits=32):
    '''
        Take the input as the MSB of a intiger of total_bits size 

        Note:
                1) total_bits = 32 is equivalent to 4 HV513, each of the witth 8 Outputs
    '''
    data_out = 0

    move = total_bits - idx -1
    data_out = (1) << move

    return data_out


def map_from_coordinates():
    '''
        Transform the the electrodoce path to be activated 
        in a bit sequence to manage the HV513 array

        Input:
            1) Coordinates (x, y)

    '''

    pass


def inverse_bits(data, total_num_bits = 8):
    a = data
    data_inverse = 0
    bit_new = 0

    for i in range(1, total_num_bits):
        read = a & 1
        # print(read)

        bit_new = read << (total_num_bits-i)
        # print(bin(bit_new))
        data_inverse = bit_new | data_inverse
        # print(bin(data_inverse))

        # next bit
        a = a >> 1
        # print("\nnext Data ", i)
        # print(bin(a))

    return data_inverse