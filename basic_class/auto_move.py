import time
import math
import PID


class Root:
	p_type_list = []  # 各阶段的移动种类；0:X,1:|,2:-,3:7,4:r,5:L,6:J
	p_parameter_list = []  # 各阶段的移动种类的参数；0:0,1:down,2:left,3:R,4:R,5:R,6:R,7:up,8:right
	p_dis_list = []  # 各阶段的移动距离
	time_cnt_list = [0]  # 各阶段累计时间
	x_list = [0]  # 各阶段x
	y_list = [0]  # 各阶段y

	def __init__(self, p_type, p_parameter, speed):
		self.p_type_list = p_type
		self.p_parameter_list = p_parameter
		self.speed = speed

		i = 0
		for type_ in self.p_type_list:  # 更新距离与时间
			parameter_ = self.p_parameter_list[i]
			if 2 < type_ < 7 or 9 < type_ < 13:
				dis = math.pi * parameter_ / 2
				self.p_dis_list.append(dis)
				if type_ == 3:
					self.x_list.append(self.x_list[len(self.x_list) - 1] + parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] - parameter_)
				elif type_ == 4:
					self.x_list.append(self.x_list[len(self.x_list) - 1] - parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] - parameter_)
				elif type_ == 5:
					self.x_list.append(self.x_list[len(self.x_list) - 1] + parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] - parameter_)
				elif type_ == 6:
					self.x_list.append(self.x_list[len(self.x_list) - 1] - parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] - parameter_)
				elif type_ == 9:
					self.x_list.append(self.x_list[len(self.x_list) - 1] - parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] + parameter_)
				elif type_ == 10:
					self.x_list.append(self.x_list[len(self.x_list) - 1] + parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] + parameter_)
				elif type_ == 11:
					self.x_list.append(self.x_list[len(self.x_list) - 1] + parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] + parameter_)
				elif type_ == 12:
					self.x_list.append(self.x_list[len(self.x_list) - 1] - parameter_)
					self.y_list.append(self.y_list[len(self.y_list) - 1] + parameter_)
				self.time_cnt_list.append(self.time_cnt_list[len(self.time_cnt_list) - 1] + dis / self.speed)
			else:
				dis = self.p_parameter_list[i]
				self.p_dis_list.append(dis)
				if type_ == 1:
					self.x_list.append(self.x_list[len(self.x_list) - 1] - parameter_)
				elif type_ == 2:
					self.y_list.append(self.y_list[len(self.y_list) - 1] - parameter_)
				elif type_ == 7:
					self.x_list.append(self.x_list[len(self.x_list) - 1] + parameter_)
				elif type_ == 8:
					self.y_list.append(self.y_list[len(self.y_list) - 1] + parameter_)
				self.time_cnt_list.append(self.time_cnt_list[len(self.time_cnt_list) - 1] + dis / self.speed)
			i += 1

	def get_stage(self, t):
		i = 0
		for time_stage in self.time_cnt_list:
			if time_stage > t:
				# print("end", i)
				break
			i += 1
		# print(self.time_cnt_list)
		x = self.x_list[i]
		y = self.y_list[i]

		try:
			degree = math.pi / 2 * (self.time_cnt_list[i] - t) / (self.time_cnt_list[i] - self.time_cnt_list[i - 1])
			# x = math.pi / 2 * (self.time_cnt_list[i] - t) / (self.time_cnt_list[i] - self.time_cnt_list[i - 1])
		except IndexError:
			print("IndexError")
			return False
		print("degree", degree)
		deg = 0
		if self.p_type_list[i - 1] == 1:  # down ok
			deg = math.pi * 1
		elif self.p_type_list[i - 1] == 2:  # left ok
			deg = math.pi * 0.5
		elif self.p_type_list[i - 1] == 3:  # down 7 ok
			deg = math.pi - degree
		elif self.p_type_list[i - 1] == 4:  # down r ok
			deg = math.pi + degree
		elif self.p_type_list[i - 1] == 5:  # down l ok
			deg = 0.5 * math.pi + degree
		elif self.p_type_list[i - 1] == 6:  # down j ok
			deg = 1.5 * math.pi - degree
		elif self.p_type_list[i - 1] == 7:  # up ok
			deg = 2 * math.pi
		elif self.p_type_list[i - 1] == 8:  # right ok
			deg = math.pi * 1.5
		elif self.p_type_list[i - 1] == 9:  # up 7 ok
			deg = 1.5 * math.pi + degree
		elif self.p_type_list[i - 1] == 10:  # up r ok
			deg = 0.5 * math.pi - degree
		elif self.p_type_list[i - 1] == 11:  # up l
			deg = 0 - degree
		elif self.p_type_list[i - 1] == 12:  # up j
			deg = degree
		print("no_move")
		return x, y, deg


class Auto:
	# type_list = [1, 6, 4, 1, 6, 5]
	type_list = [1]
	parameter_list = [1]
	# parameter_list = [0.3, 2.2, 0.5, 0.5, 1, 0.5]
	speed = 1

	def __init__(self, tcp, udp, printing=True):  #
		self.x_pid = PID.PID(4, 0, 0)
		self.y_pid = PID.PID(4, 0, 0)
		self.msg = None
		self.tcp = tcp
		self.udp = udp
		self.tcp.IN_OUT("robot mode free;", printing=printing)
		# self.tcp.IN_OUT("chassis push position on pfreq 50;", printing=printing)
		self.root = Root(self.type_list, self.parameter_list, self.speed)

	def solve_chassis_position(self, printing=True):
		result = ''
		if self.msg[0:22] == 'chassis push position ' and self.msg[-1] == ';':
			# print('right_start')
			info = self.msg[22:-3]
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

	def move(self, printing=True):
		moving = True
		start_time = time.perf_counter()
		while moving:
			self.msg = self.udp.try_get(timeout=1, printing=False)
			# print(self.msg)
			x_y = self.solve_chassis_position(printing=False)
			print("xy:", x_y)

			now_time = time.perf_counter() - start_time
			# print("time:-------", now_time)
			target_x, target_y, dir_ = self.root.get_stage(now_time)
			x_out = self.x_pid.pid_control(target_x - x_y[0])
			y_out = self.y_pid.pid_control(target_y - x_y[1])
			print(round(dir_ / math.pi * 180, 2))
			x = self.speed * math.sin(dir_)
			y = self.speed * math.cos(dir_)
			self.tcp.IN_OUT("chassis speed x " + str(y + x_out) + " y " + str(x + y_out) + ";", printing=printing)
			# print(result)
			# print("dir", dir_)
			if not dir_:
				print("False")
				moving = False
			# time.sleep(0.1)
		return True


if __name__ == "__main__":
	auto = Auto()
	result = auto.move()
	print("result", result)
