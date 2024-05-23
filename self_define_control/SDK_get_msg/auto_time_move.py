import time

import MSG_Solve
import Message_Delivery
import SDK_

# import matplotlib.pyplot as plt

kp = 0.5
target = 0.5
error_list = []

SDK_.connect_enter_SDK(printing=False)
Message_Delivery.connect_UDP(printing=False)
SDK_.IN_OUT("game_msg on;", printing=False)
SDK_.IN_OUT("chassis push position on pfreq 50;", printing=False)
SDK_.IN_OUT("robot mode free;", printing=False)

start_time = time.perf_counter()

now_time = time.perf_counter() - start_time

for i in range(1, 150):
	print(i)
	now_time = time.perf_counter() - start_time
	x_target = (0.25 * (now_time - 2) ** 2 - 1) * 5
	msg = Message_Delivery.try_get(timeout=1, printing=False)
	chassis_position = []
	chassis_position = MSG_Solve.solve_chassis_position(msg, printing=False)
	print(chassis_position)
	# chassis speed x 0.1 y 0.1 z 1;
	if chassis_position != []:
		error = x_target - chassis_position[0]
		error_list.append(error)
		x_speed = kp * error
		print("--------------", x_speed)
		SDK_.IN_OUT("chassis speed x " + str(x_speed) + " y 0 z 0;", printing=True)
print(error_list)
# plt.plot(range(1,200),error_list)
# plt.show()
