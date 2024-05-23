import robot_connection
import solve
import Chassis_Solve
import time
import os
# import auto_aim
import RobotLiveview
# import tmp_fast2
import PID


def example():
	print("start")
	robot = robot_connection.RobotConnection('192.168.42.2')
	robot.open()

	robot.send_data('command;')
	print('send data to robot   : command')

	robot.send_data('game_msg on;')
	print('send data to robot   : game_msg on')

	while True:
		msg = robot.recv_push_data(5)
		if msg:
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
	auto_aim.connect()
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
				auto_aim.auto_aim()
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
	yaw_PID = PID.PID(20, 0, 0)
	pitch_PID = PID.PID(20, 0, 0)
	print("start")
	robot = robot_connection.RobotConnection('192.168.42.2')
	robot.open()
	robot.send_data('command;')
	'''time.sleep(1)
	robot.send_data('quit;')
	time.sleep(1)
	robot.send_data('command;')'''
	time.sleep(1)
	# print('send data to robot   : command')
	robot.send_data('game_msg on;')
	robot.send_data('robot mode free;')
	time.sleep(1)
	robot_liveview = RobotLiveview.RobotLiveview(3, robot)
	# print('send data to robot   : game_msg on')
	robot_liveview.open()
	robot_liveview.display()
	while True:
		msg = robot.recv_push_data(5)

		# print("msg:",msg)
		if msg:
			msg = str(msg, encoding="utf-8")
			msg_solved = solve.solve_game_msg(msg, printing=False)
		# print("msg_solved:",msg_solved)

		pos_arr = robot_liveview.get_target()
		print("target information:", pos_arr)
		if len(pos_arr) == 0:
			continue
		aim = False
		if msg:
			if "E" in msg_solved["keys"]:
				print("E:auto_aim")
				aim = True
		aim = True
		if float(pos_arr[0]) != 0 and aim:
			posx = (float(pos_arr[0]) - 640) / 640
			posy = (float(pos_arr[1]) - 360) / 360
			print("------------------x,y:", posx, posy)
			yaw = int(yaw_PID.control(posx))
			pitch = -int(pitch_PID.control(posy))
			print("yaw,pitch:", yaw, pitch)
			robot.send_data('gimbal speed p ' + str(pitch) + ' y ' + str(yaw) + ';')

	UDP.disconnect()
	TCP.disconnect()


# tmp_fast2.test()

if __name__ == '__main__':
	# chassis_controll()
	video_test()
