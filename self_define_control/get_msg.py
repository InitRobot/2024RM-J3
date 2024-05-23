# -*- encoding: utf-8 -*-
# 测试环境：Python 3.6 版本

import socket
import sys

# 组网模式下，机器人当前 IP 地址为 192.168.1.176, 控制命令端口号为 40923
# 机器人 IP 地址根据实际 IP 进行修改
host = "192.168.1.176"
port = 40923


def connect():
	global s
	address = (host, int(port))

	# 与机器人控制命令端口建立 TCP 连接
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
	msg = "game_msg on;"
	aasgrb = s.send(msg.encode('utf-8'))
	print('send')
	msg = "game msg push [cmdid,len, mouse_press, mouse_x, mouse_y];"
	s.send(msg.encode('utf-8'))
	print("msg")
	print('a:', aasgrb)
	try:
		# 等待机器人返回执行结果
		print('try')
		buf = s.recv(1024)
		print('buf')
		print(buf.decode('utf-8'))
	except socket.error as e:
		print("Error receiving :", e)
		sys.exit(1)


if __name__ == '__main__':
	connect()
	i = 0
	print('1')
	msg = "commend;"
	s.send(msg.encode('utf-8'))
	while (i <= 1000):
		i += 1
		print('s')
		get_msg()
		print(i)
		if ():
			print('break')
			break
	disconnect()
