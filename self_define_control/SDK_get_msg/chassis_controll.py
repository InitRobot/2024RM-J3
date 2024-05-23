import Chassis_Move
import Chassis_Solve
import MSG_Solve
import Message_Delivery
import SDK_

SDK_.connect_enter_SDK(printing=False)
Message_Delivery.connect_UDP(printing=False)
SDK_.IN_OUT("game_msg on;", printing=False)
SDK_.IN_OUT("robot mode free;", printing=False)
SDK_.IN_OUT("robot mode gimbal_lead;")
while True:
	game_msg = Message_Delivery.try_get(timeout=1, printing=False)
	# print(game_msg)
	game_msg = MSG_Solve.solve_game(game_msg, printing=False)
	# print(game_msg)
	key_list = MSG_Solve.solve_key(game_msg, printing=False)
	key_name_list = MSG_Solve.solve_key_name(key_list)
	# print(key_name_list)
	# print('1')
	gimbal_msg = SDK_.IN_OUT("gimbal attitude ?;", printing=False)
	gimbal = MSG_Solve.solve_gimbal(gimbal_msg, printing=False)

	# Try W
	# key_name_list = ['D']

	# wheel_spin = Chassis_Solve.Disk_solve(key_name_list, gimbal[1])
	wheel_spin = Chassis_Solve.Stright_Solve(key_name_list, printing=False)
	print(wheel_spin)
	Chassis_Move.move(wheel_spin, printing=False)

Chassis_Move.move([0, 0, 0, 0])
SDK_.IN_OUT("game_msg off;")
Message_Delivery.disconnect()
SDK_.disconnect()
