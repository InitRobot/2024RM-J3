import MSG_Solve
import Message_Delivery
import SDK_

# import time


SDK_.connect_enter_SDK()
Message_Delivery.connect_UDP()
# SDK_.IN_OUT("chassis status ?;")
SDK_.IN_OUT("game_msg on;")
# SDK_.IN_OUT("chassis push freq 10;")
# time.sleep(1)
for i in range(1, 50):
	# print("try TCP")
	# SDK_.OUT(timeout = 1)
	# print("try UDP")
	game_msg = Message_Delivery.try_get(timeout=1)
	# print(game_msg)
	game_msg = MSG_Solve.solve_game(game_msg)
	print(game_msg)
	key_list = MSG_Solve.solve_key(game_msg)
	if 87 in key_list:
		print('right')
		SDK_.IN_OUT("gimbal move p 10;")
# SDK_.IN_OUT("game msg push [0, 6, 1, 0, 0, 255, 1, 199];")
SDK_.IN_OUT("game_msg off;")
Message_Delivery.disconnect()
SDK_.disconnect()
