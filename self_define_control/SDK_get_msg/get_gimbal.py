import MSG_Solve
import SDK_

SDK_.connect_enter_SDK(printing=False)
SDK_.IN_OUT("robot mode free;", printing=False)

for i in range(1, 500):
	gimbal_msg = SDK_.IN_OUT("chassis position ?;", printing=False)
	gimbal = MSG_Solve.solve_gimbal(gimbal_msg, printing=False)
	print(gimbal)

SDK_.disconnect()
