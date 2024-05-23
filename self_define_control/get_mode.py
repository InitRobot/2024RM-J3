# -*- encoding: utf-8 -*-
# 测试环境：Python 3.6 版本

import socket

# 组网模式下，机器人当前 IP 地址为 192.168.1.176, 控制命令端口号为 40923
# 机器人 IP 地址根据实际 IP 进行修改
host = "192.168.1.176"
port_TCP = 40923
port_UDP = 40924


def connect_TCP():
	global s
	address = (host, int(port_TCP))

	# 与机器人控制命令端口建立 TCP 连接
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print("Connecting...")

	s.connect(address)

	print("Connected!")


def connect_UDP():
	global s
	address = (host, int(port_UDP))

	# 与机器人控制命令端口建立 UDP 连接
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	print("Connecting...")

	s.connect(address)

	print("Connected!")


def disconnect():
	global s
	s.shutdown(socket.SHUT_WR)
	s.close()
	print('dis')


def get_msg():
	global s
	msg = "chassis attitude ?;"
	print(msg.encode('utf-8'))
	a = s.send(msg.encode('utf-8'))
	return (a)


# print('send')
# print("msg")


if __name__ == '__main__':
	connect_TCP()
	i = 0
	# print('1')
	msg = "command;"
	s.send(msg.encode('utf-8'))
	while (i <= 9):
		i += 1
		# print('s')
		print(i, ':', get_msg())
		# print(i)
		if ():
			print('break')
			break
	disconnect()
