import math
from connect import TCP_connection, UDP_connection

forward_speed = 90
backward_speed = 50
side_speed = 50


def Stright_Solve(TCP, degree, keys, printing=True):
	speed_stright = 2
	# SDK_.IN_OUT("gimbal recenter;")
	# TCP.IN_OUT("robot mode free;", printing=printing)
	result = []
	# 对应    左右
	wheel = [0, 0,  # 前(head)
	         0, 0]  # 后(tail)
	# 对应    左右
	wheel2 = [0, 0,  # 前(head)
	          0, 0]  # 后(tail)
	# print(degree)
	if abs(degree) >= 2:
		kp = 0.02
		wheel2[0] = degree * kp
		wheel2[1] = 0 - degree * kp
		wheel2[2] = degree * kp
		wheel2[3] = 0 - degree * kp
	if 'W' in keys:
		wheel = [(i + 1) for i in wheel]
	if 'A' in keys:
		wheel[0] -= 1
		wheel[1] += 1
		wheel[2] += 1
		wheel[3] -= 1
	if 'S' in keys:
		wheel = [(i - 1) for i in wheel]
	if 'D' in keys:
		wheel[0] += 1
		wheel[1] -= 1
		wheel[2] -= 1
		wheel[3] += 1
	for i in range(len(wheel)):
		if wheel[i] > 0:
			wheel[i] = speed_stright + wheel2[i]
		elif wheel[i] < 0:
			wheel[i] = -speed_stright + wheel2[i]
		else:
			wheel[i] = wheel2[i]
	if printing:
		print(wheel)
	result = wheel
	return result


def Disk_solve(TCP, keys, degree, spin=1, printing=True):
	speed_disk = 2
	speed_spin = 1.5
	# TCP.IN_OUT("robot mode free;", printing=printing)
	# 对应        左右
	wheel_stright = [0, 0,  # 前(head)
	                 0, 0]  # 后(tail)
	wheel_spin = wheel_stright
	wheel_stright_W = wheel_stright
	wheel_stright_A = wheel_stright
	wheel_stright_S = wheel_stright
	wheel_stright_D = wheel_stright
	wheel_stright = []
	if 'A' in keys:
		wheel_stright_A[0] = math.sin((degree / 180 - 0.25) * math.pi)
		wheel_stright_A[1] = math.sin((degree / 180 + 0.25) * math.pi)
		wheel_stright_A[2] = math.sin((degree / 180 + 0.25) * math.pi)
		wheel_stright_A[3] = math.sin((degree / 180 - 0.25) * math.pi)
		wheel_stright.append(wheel_stright_A)
	if 'W' in keys:
		degreew = degree + 90
		wheel_stright_W[0] = math.sin((degreew / 180 - 0.25) * math.pi)
		wheel_stright_W[1] = math.sin((degreew / 180 + 0.25) * math.pi)
		wheel_stright_W[2] = math.sin((degreew / 180 + 0.25) * math.pi)
		wheel_stright_W[3] = math.sin((degreew / 180 - 0.25) * math.pi)
		wheel_stright.append(wheel_stright_W)

	if 'S' in keys:
		degrees = degree - 90
		wheel_stright_S[0] = math.sin((degrees / 180 - 0.25) * math.pi)
		wheel_stright_S[1] = math.sin((degrees / 180 + 0.25) * math.pi)
		wheel_stright_S[2] = math.sin((degrees / 180 + 0.25) * math.pi)
		wheel_stright_S[3] = math.sin((degrees / 180 - 0.25) * math.pi)
		wheel_stright.append(wheel_stright_S)

	if 'D' in keys:
		degreed = degree - 180
		wheel_stright_D[0] = math.sin((degreed / 180 - 0.25) * math.pi)
		wheel_stright_D[1] = math.sin((degreed / 180 + 0.25) * math.pi)
		wheel_stright_D[2] = math.sin((degreed / 180 + 0.25) * math.pi)
		wheel_stright_D[3] = math.sin((degreed / 180 - 0.25) * math.pi)
		wheel_stright.append(wheel_stright_D)

	if printing:
		print('str', wheel_stright)
	if len(keys) == 2 or len(keys) == 4 or len(keys) == 5:
		wheel_spin = wheel_stright[-1]
	elif len(keys) == 3:
		for i in range(0, 4):
			wheel_spin[i] = (wheel_stright[1][i] + wheel_stright[2][i]) / 2
	# print(wheel_spin)
	# spin
	if printing:
		print('sp', wheel_spin)
	wheel_spin[0] = (wheel_spin[0] * speed_disk + 1 * speed_spin) / 2
	wheel_spin[1] = (wheel_spin[1] * speed_disk - 1 * speed_spin) / 2
	wheel_spin[2] = (wheel_spin[2] * speed_disk + 1 * speed_spin) / 2
	wheel_spin[3] = (wheel_spin[3] * speed_disk - 1 * speed_spin) / 2

	return wheel_spin


speed = 10


def move(TCP, wheel, printing=True):
	wheel = [i * 1000 / 100 * speed for i in wheel]
	chassis = "chassis wheel w2 " + str(wheel[0]) + " w1 " + str(wheel[1]) + " w3 " + str(wheel[2]) + " w4 " + str(
		wheel[3]) + ";"
	TCP.IN_OUT(chassis, printing=printing)
