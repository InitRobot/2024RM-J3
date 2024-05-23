import socket
import sys

# USB 模式下，机器人默认 IP 地址为 192.168.42.2, 控制命令端口号为 40923
host = "192.168.42.2"
port = 40923


# other code

def connect_TCP():  # 与机器人控制命令端口建立 TCP 连接
	global s
	address = (host, int(port))

	# 与机器人控制命令端口建立 TCP 连接
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print("Connecting...")

	s.connect(address)

	print("Connected!")


def disconnect():  # 关闭端口连接
	global s
	# 关闭端口连接
	s.shutdown(socket.SHUT_WR)
	s.close()


def try_get():  # 等待机器人返回执行结果
	result = ''
	try:
		# 等待机器人返回执行结果
		buf = s.recv(1024)
		result = (buf.decode('utf-8'))
	except socket.error as e:
		print("Error receiving :", e)
		sys.exit(1)
	return result


def IN(message):  # 检测并向机器发送message，并输出
	# in_message为要发送的指令
	if (str(type(message)) == "<class 'str'>") and (message[-1] == ';'):
		print('IN:', message)
		s.send(message.encode('utf-8'))
	else:
		print('please input str that ends with ";"')


def OUT():  # 检测机器回复，并输出
	result = ''
	result = try_get()
	print("OUT:", result)
	return result


def IN_OUT(message):  # 检测并向机器发送message，检测机器回复，并输出
	result = ''
	IN(message)
	result = OUT()
	return result


def connect_enter_SDK():  # 与机器人控制命令端口建立 TCP 连接，并进入SDK模式控制
	connect_TCP()
	IN_OUT("command;")
