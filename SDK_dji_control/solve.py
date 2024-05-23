def solve_game(msg, printing=True):  # 用于解析赛事数据推送
	result = ''
	solveablility = True
	if msg[0:14] == 'game msg push ' and msg[-1] == ';':
		# print('right_start')
		info = msg[15:-2]
		# print(info)
		info_list = info.split(', ')
		# print(info_list)
		info_list_int = [int(i) for i in info_list]
		# print(info_list_int)
		result = info_list_int
	else:
		solveablility = False
		if printing:
			print('please give a game msg push')
	return result, solveablility


def solve_information(msg, printing=True):  # 用于从赛事数据推送1中获得信息
	result = {
		"time": "",
		"health": "",
		"ammo": ""
	}

	if msg[0] != 1 or msg[1] != 11:

		if printing:
			print("unsolveable")
		return result
	else:
		result["time"] = msg[3]
		result["health"] = msg[7]
		result["ammo"] = msg[9]
	return result


def solve_key(msg, printing=True):  # 用于从赛事数据推送0中获得键位
	result = []
	key_n = msg[6]
	if printing:
		print(key_n)
	if key_n != 0:
		keys = msg[0 - key_n:]
		if printing:
			print(keys)
			print(type(keys))
		result = keys
	return result


def solve_key_name(keys, printing=True):  # 将获得键位转换为真实名称
	result = {
		"keys": []
	}
	key_name_list = []
	for key in keys:
		if key >= 48 and key <= 90:
			key_name_list.append(chr(key))
		elif key == 8:
			key_name_list.append("Space")
		elif key == 9:
			key_name_list.append("Tab")
		elif key == 16:
			key_name_list.append("Shift")
		elif key == 17:
			key_name_list.append("Ctrl")
		elif key == 18:
			key_name_list.append("Alt")
		elif key == 20:
			key_name_list.append("Caps")
	if printing:
		print(key_name_list)
	result["keys"] = key_name_list
	return result


def solve_game_msg(msg, printing=True):
	result = {
		"time": "",
		"health": "",
		"ammo": "",
		"keys": [],
		"mouse_keys": "",
		"mouse_move": [0, 0],
	}
	solveablity = True
	msg_solved, solveablity = solve_game(msg, printing=printing)
	# msg_solved = msg

	if solveablity and msg_solved[0] == 1:
		# print(msg)
		msg_information = solve_information(msg_solved, printing=printing)
		if printing:
			print(msg_information)
		result.update(msg_information)
	elif solveablity and msg_solved[0] == 0:

		msg_keys = solve_key(msg_solved, printing=printing)
		msg_keys_name = solve_key_name(msg_keys, printing=printing)
		if printing:
			print(msg_keys_name)
		result.update(msg_keys_name)
		result["mouse_keys"] = msg_solved[2]
		result["mouse_move"] = msg_solved[3:5]
	return result


def solve_gimbal(msg, printing=True):
	result = ''
	if msg[-1] == ';':
		if printing:
			print('right_start')
		info = msg[:-2]
		if printing:
			print(info)
		info_list = info.split(' ')
		if printing:
			print(info_list)
		info_list_int = [float(i) for i in info_list]
		if printing:
			print(info_list_int)
		result = info_list_int
	else:
		if printing:
			print('please give a gimbal msg push')
	return result


def solve_chassis_position(msg, printing=True):
	result = ''
	if msg[0:22] == 'chassis push position ' and msg[-1] == ';':
		# print('right_start')
		info = msg[22:-3]
		if printing:
			print(info)
		info_list = info.split(' ')
		if printing:
			print(info_list)
		info_list_float = []
		for i in info_list:
			if printing:
				print(i)
			if i != "-0.000" and i != "0.000":
				if printing:
					print("float")
				if i[0] == '-':
					info_list_float.append(-float(i[1:]))
				else:
					info_list_float.append(float(i))
			else:
				info_list_float.append(0)
		if printing:
			print(info_list_float)
		result = info_list_float
	else:
		if printing:
			print('please give a chassis push position push')
	return result
