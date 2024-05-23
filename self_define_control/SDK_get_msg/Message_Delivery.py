import socket
import sys

import select

# USB 模式下，机器人默认 IP 地址为 192.168.42.2, 消息推送端口号为 40924
host = "0.0.0.0"
port = 40924


def connect_UDP(printing=True):  # 与机器人控制命令端口建立 UDP 连接
	global udp_socket
	address = (host, int(port))

	# 与机器人控制命令端口建立 UDP 连接
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	if printing:
		print("Connecting_UDP...")

	udp_socket.bind(address)

	if printing:
		print("UDP_Connected!")


def try_get(timeout=5, printing=True):  # 这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回空字符串。如果收到了机器人的返回结果，就会解码并返回结果字符串。
	result = ''
	try:
		# 设置超时时间
		ready = select.select([udp_socket], [], [], timeout)
		# print(ready)
		if ready[0]:
			# 如果有可读数据，接收并解码
			# print("hearing...")
			buf = udp_socket.recv(1024)
			result = buf.decode('utf-8')
		else:
			result = 'no_OUT'
	except socket.error as e:
		if printing:
			print("Error receiving :", e)
		sys.exit(1)
	if printing:
		print(result)
	return result


def disconnect(printing=True):
	if printing:
		print("UDP disconnecting...")
	udp_socket.close()
	if printing:
		print("UDP disconnected!")
