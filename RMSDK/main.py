from robomaster import robot


def robot_control(run):
	if run == ord('w'):
		print("forward！")
		ep.chassis.drive_speed(0.5, 0, 0)
	elif run == ord('s'):
		print("back！")
		ep.chassis.drive_speed(-0.5, 0, 0)
	elif run == ord('a'):
		print("left")
		ep.chassis.drive_speed(0, -0.5, 0)
	elif run == ord('d'):
		print("right！")
		ep.chassis.drive_speed(0, 0.5, 0)
	elif run == 0:
		print("stop！")
		ep.chassis.drive_speed(0, 0, 0)


def sub_data_handler(sub_info):
	"""    返回数据 (buf: 键鼠数据 [mouse_press, mouse_x, mouse_y, seq, key_num, key_1, key2, ….])
		   mouse_press: 1为鼠标右键, 2为鼠标左键, 4为鼠标中间
		   mouse_x : 鼠标移动距离, 范围-100 ~ 100
		   mouse_y : 鼠标移动距离, 范围-100 ~ 100
		   seq: 序列号 0~255
		   key_num: 识别到的按键数, 最多识别三个按键
		   key1: 被按下的键盘键值
	"""
	print("mouse_press:{0} mouse_x:{1} mouse_y:{2} key1:{3}"
	      .format(sub_info[0], sub_info[1], sub_info[2], sub_info[-1]))
	robot_control(sub_info[-1])


if __name__ == '__main__':
	ep = robot.Robot()
	ep.initialize(conn_type="rndis")
	# ep.chassis.stick_overlay(1)
	ep.set_robot_mode(mode=robot.GIMBAL_LEAD)
	ep.sub_game_msg(callback=sub_data_handler)
