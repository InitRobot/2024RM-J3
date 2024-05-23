import connect
import solve
import Chassis_Solve
import time
import os
# import auto_aim
import RobotLiveview
import auto_move


# import tmp_fast2

def example():
	"""
	以下为连接TCP,UDP获取赛事引擎数据的示例
	"""
	print("start")
	TCP = connect.TCP_connection(printing=False)
	UDP = connect.UDP_connection(printing=False)
	TCP.connect_enter_SDK(printing=False)
	UDP.connect(printing=False)
	TCP.IN_OUT("game_msg on;", printing=False)
	# for i in range(1, 50):
	while True:
		msg = UDP.try_get(timeout=1, printing=False)
		# print(msg)
		if msg != "no_OUT":
			msg_solved = solve.solve_game_msg(msg, printing=False)
			print(msg_solved)
	UDP.disconnect()
	TCP.disconnect()


# -------以上为示例--------
'''
            msg_solved = solve.solve_game(msg,printing=False)
            if msg_solved[0] == 0:
                keys = solve.solve_key(msg_solved,printing=False)
                keyname = solve.solve_key_name(keys,printing=False)
                print("keynames:", keyname)
            elif msg_solved[0] == 1:
                print("Unknow:",msg_solved)
            else:
                print("-----???-----",msg_solved)'''


def chassis_controll():
	print("start")
	TCP = connect.TCP_connection(printing=False)
	UDP = connect.UDP_connection(printing=False)
	TCP.connect_enter_SDK(printing=False)
	UDP.connect(printing=False)
	TCP.IN_OUT("game_msg on;", printing=False)
	# for i in range(1, 50):
	disk_mode = False
	wait = 0
	TCP.IN_OUT("robot mode free;", printing=True)
	# auto_aim.connect()
	print("connected")
	while True:
		# time.sleep(0.1)
		msg = UDP.try_get(timeout=1, printing=False)
		print(msg)
		# print(msg)
		if msg != "no_OUT":
			msg_solved = solve.solve_game_msg(msg, printing=False)
			if wait > 0:
				wait -= 1
			# print(msg_solved["keys"], "---", wait)
			if "M" in msg_solved["keys"] and wait == 0:
				# print(msg_solved["keys"], "---", wait)
				disk_mode = not disk_mode
				wait = 10
				print("mode_change")
				if not disk_mode:
					pass
			# print(msg_solved)

			if "E" in msg_solved["keys"]:
				print("E:auto_aim")
			# auto_aim.auto_aim()
			# os.system('cd ~/RM-yolo/RMSDK && python3 06_final.py')

			if disk_mode:
				degree = solve.solve_gimbal(TCP.IN_OUT("gimbal attitude ?;", printing=False), printing=False)
				wheel_output = Chassis_Solve.Disk_solve(TCP, msg_solved["keys"], degree[1], printing=False)
			elif not disk_mode:
				degree = solve.solve_gimbal(TCP.IN_OUT("gimbal attitude ?;", printing=False), printing=False)
				wheel_output = Chassis_Solve.Stright_Solve(TCP, degree[1], msg_solved["keys"], printing=False)
			# print(wheel_output)
			Chassis_Solve.move(TCP, wheel_output, printing=False)
	UDP.disconnect()
	TCP.disconnect()


def video_test():
	print("start")
	TCP = connect.TCP_connection(printing=True)
	TCP_video = connect.TCP_video(printing=True)
	UDP = connect.UDP_connection(printing=True)
	TCP.connect_enter_SDK(printing=True)
	UDP.connect(printing=True)
	TCP_video.connect(printing=True)
	TCP.IN_OUT("game_msg on;", printing=True)
	TCP.IN_OUT("stream on;", printing=True)
	robot = RobotLiveview.RobotLiveview(TCP_video)
	print("connected view")
	robot.display(TCP)
	# tmp_fast2.test()
	while True:
		pass


def solve(x, a, b, c, d):
	y = ((b - d) / ((a - c) ** 2)) * ((x - c) ** 2) + d
	return y


def target_xy(t, mode=1):
	Flag_move = False
	x_t = 0
	y_t = 0
	if mode == 1:
		Flag_move = True
		point = -1
		step = 0
		point_1 = 0
		time_changes = [0, 3.3, 4, 4.7, 5.5]
		x_joints = [0, -1.8, -2.5, -3, -1.7]
		y_joints = [0, -1.45, -2, -3, -5]
		for t_c in time_changes:
			point_1 += 1
			if t < t_c:
				point = point_1
				break
		if point != -1:
			if point == 0:
				step = 1
				x_t = (solve(t, time_changes[step], x_joints[step], time_changes[step + 1], x_joints[step + 1]))
				y_t = (solve(t, time_changes[step + 1], y_joints[step + 1], time_changes[step], y_joints[step]))
			if point == 1:
				step = 2
				x_t = (solve(t, time_changes[step], x_joints[step], time_changes[step + 1], x_joints[step + 1]))
				y_t = (solve(t, time_changes[step + 1], y_joints[step + 1], time_changes[step], y_joints[step]))
			if point == 2:
				step = 3
				x_t = (solve(t, time_changes[step], x_joints[step], time_changes[step + 1], x_joints[step + 1]))
				y_t = (solve(t, time_changes[step + 1], y_joints[step + 1], time_changes[step], y_joints[step]))
			if point == 3:
				step = 4
				x_t = (solve(t, time_changes[step], x_joints[step], time_changes[step + 1], x_joints[step + 1]))
				y_t = (solve(t, time_changes[step + 1], y_joints[step + 1], time_changes[step], y_joints[step]))
		else:
			x_t = x_joints[-1]
			y_t = y_joints[-1]

	return Flag_move, x_t, y_t


"""
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
"""


def auto_move_():
	print("start")
	TCP = connect.TCP_connection(printing=False)
	UDP = connect.UDP_connection(printing=False)
	TCP.connect_enter_SDK(printing=False)
	UDP.connect(printing=False)
	TCP.IN_OUT("chassis push position on pfreq 50;", printing=False)
	TCP.IN_OUT("robot mode free;", printing=True)
	# TCP.IN_OUT("game_msg on;",printing=False)
	# for i in range(1, 50):
	# disk_mode = False
	# wait = 0
	auto = auto_move.Auto(TCP, UDP)
	end = auto.move()

	second_step_time = 5
	TCP.IN_OUT("chassis speed x 0 y 0 z 0;", printing=False)
	TCP.IN_OUT("chassis push position off;", printing=True)
	# print(error_list)
	print('end')


def chassis_pos():
	print("start")
	TCP = connect.TCP_connection(printing=False)
	UDP = connect.UDP_connection(printing=False)
	TCP.connect_enter_SDK(printing=False)
	UDP.connect(printing=False)
	TCP.IN_OUT("chassis push position on pfreq 50;", printing=False)
	# TCP.IN_OUT("gimbal push attitude on;", printing=False)
	# for i in range(1, 50):
	disk_mode = False
	wait = 0
	TCP.IN_OUT("robot mode free;", printing=True)
	# auto_aim.connect()
	print("connected")
	while True:
		# time.sleep(0.1)
		msg = UDP.try_get(timeout=1, printing=False)
		print(msg)
		# x_y = solve.solve_gimbal(msg, printing=False)
		x_y = solve_chassis_position(msg, printing=False)

		print(x_y)
		# print(msg)
	UDP.disconnect()
	TCP.disconnect()


if __name__ == '__main__':
	# chassis_controll()
	# video_test()
	auto_move_()
	# chassis_pos()
