import time

import HVbase_lib


semi_period = 1

# Remember update the pins numbers in the constructure function
device_hv513 = HVbase_lib.HV513()

device_hv513.setup()
device_hv513.reset()

device_hv513.set_GPIO(device_hv513.CLK, 0)
time.sleep(semi_period)
device_hv513.set_GPIO(device_hv513.CLK, 1)
time.sleep(semi_period)


# device_hv513.set_GPIO(device_hv513.LE, 0)
# time.sleep(semi_period)
# device_hv513.set_GPIO(device_hv513.LE, 1)
# time.sleep(semi_period)


# device_hv513.set_GPIO(device_hv513.DATA, 0)
# time.sleep(semi_period)
# device_hv513.set_GPIO(device_hv513.DATA, 1)
# time.sleep(semi_period)


# while(True):
#     device_hv513.set_GPIO(device_hv513.CLK, 0)
#     time.sleep(semi_period)
#     device_hv513.set_GPIO(device_hv513.CLK, 1)
#     time.sleep(semi_period)

