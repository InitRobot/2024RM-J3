import os
import re
import socket

import select

global tcp_socket
global udp_socket


def tcp_connect():
	# 与机器人控制命令端口建立 TCP 连接
	tcp_address = ("192.168.42.2", int(40923))
	global tcp_socket
	tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("TCP Connecting...")
	tcp_socket.connect(tcp_address)
	print("TCP Connected!")


def udp_connect():
	# 与机器人控制命令端口建立 UDP 连接
	udp_address = ("0.0.0.0", int(40924))
	global udp_socket
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print("UDP Connecting...")
	udp_socket.bind(udp_address)
	print("UDP Connected!")


def start_get_game_msg():
	# 进入明文模式
	msg = "command;"
	tcp_socket.send(msg.encode('utf-8'))
	buf = tcp_socket.recv(1024)
	print(buf.decode('utf-8'))

	msg = "quit;"
	tcp_socket.send(msg.encode('utf-8'))
	buf = tcp_socket.recv(1024)
	print(buf.decode('utf-8'))

	msg = "command;"
	tcp_socket.send(msg.encode('utf-8'))
	buf = tcp_socket.recv(1024)
	print(buf.decode('utf-8'))

	# 开始赛事推送
	msg = "game_msg on;"
	tcp_socket.send(msg.encode('utf-8'))
	buf = tcp_socket.recv(1024)
	print(buf.decode('utf-8'))


def main():
	tcp_connect()
	udp_connect()
	start_get_game_msg()
	while True:
		# print("Waiting msg")
		# 设置超时时间
		ready = select.select([udp_socket], [], [], 5)
		if ready[0]:
			# 接收数据并转为数组
			buf = udp_socket.recv(1024)
			game_msg = re.findall(r"\d+", buf.decode('utf-8'))
			print(game_msg)
			if int(game_msg[6]) > 0:
				key_num = [0] * 3
				for i in range(7, 7 + int(game_msg[6]), 1):
					key_num[i - 7] = int(game_msg[i])
				print(key_num)
				# 判断按下的按键并触发对应函数
				if 81 in key_num:  # 按下Q
					os.system('cd ~/RM-yolo/RMSDK && python3 06_final.py')

	# 关闭端口连接
	tcp_socket.shutdown(socket.SHUT_WR)
	tcp_socket.close()
	udp_socket.shutdown(socket.SHUT_WR)
	udp_socket.close()
	print("Socket Closed")


if __name__ == '__main__':
	main()
