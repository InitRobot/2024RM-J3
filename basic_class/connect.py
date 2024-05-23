import socket
import sys
import queue
import select
import threading


class TCP_connection:
	# USB 模式下，机器人默认 IP 地址为 192.168.42.2, 控制命令端口号为 40923
	host = "192.168.42.2"
	port = 40923
	printing = True
	connection = False

	def __init__(self, printing=True):
		self.printing = printing

	def connect(self, printing=True):  # 与机器人控制命令端口建立 TCP 连接
		self.address = (self.host, int(self.port))
		self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.printing or printing:
			print("Connecting_TCP...")

		self.TCP_socket.connect(self.address)
		self.connection = True
		if self.printing or printing:
			print("TCP_Connected!")

	def disconnect(self, printing=True):  # 与机器人控制命令端口断开 TCP 连接
		if not self.connection:
			if self.printing or printing:
				print("You Haven't Connected Yet")
			return
		if self.printing or printing:
			print("TCP_disconnecting...")
		self.TCP_socket.shutdown(socket.SHUT_WR)
		self.TCP_socket.close()
		if self.printing or printing:
			print("TCP_disconnected!")

	def IN(self, message, printing=True):  # 检测并向机器发送message
		if not self.connection:
			if self.printing or printing:
				print("You Haven't Connected Yet")
			return
		if (str(type(message)) == "<class 'str'>") and (message[-1] == ';'):
			if self.printing or printing:
				print('IN:', message)
			self.TCP_socket.send(message.encode('utf-8'))
		else:
			if self.printing or printing:
				print('please input str that ends with ";"')

	def try_get_message(self, timeout=5,
	                    printing=True):  # 这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。
		if not self.connection:
			if self.printing or printing:
				print("You Haven't Connected Yet")
			return
		result = ''
		try:
			# 设置超时时间
			ready = select.select([self.TCP_socket], [], [], timeout)
			if ready[0]:
				# 如果有可读数据，接收并解码
				buf = self.TCP_socket.recv(10240)
				result = buf.decode('utf-8')
			else:
				result = 'no_OUT'
		except socket.error as e:
			if self.printing or printing:
				print("Error receiving :", e)
			sys.exit(1)
		return result

	def OUT(self, timeout=5, printing=True):  # 检测机器回复
		if not self.connection:
			if self.printing or printing:
				print("You Haven't Connected Yet")
			return
		result = ''
		result = self.try_get_message(timeout)
		if self.printing or printing:
			print("OUT:", result)
		return result

	def IN_OUT(self, message, timeout=5, printing=True):  # 检测并向机器发送message，检测机器回复
		if not self.connection:
			if self.printing or printing:
				print("You Haven't Connected Yet")
			return
		result = ''
		self.IN(message, printing=self.printing)
		result = self.OUT(timeout=timeout, printing=self.printing)
		return result

	def connect_enter_SDK(self, timeout=5, printing=True):  # 与机器人控制命令端口建立 TCP 连接，并进入SDK模式控制
		if not self.connection:
			if self.printing or printing:
				print("You Haven't Connected Yet")
			self.connect(printing=self.printing)
		self.IN_OUT("command;", timeout=timeout, printing=self.printing)
		self.IN_OUT("quit;", timeout=timeout, printing=self.printing)  # 以免图传卡住
		self.IN_OUT("command;", timeout=timeout, printing=self.printing)


class UDP_connection:
	# USB 模式下，机器人默认 IP 地址为 192.168.42.2, 消息推送端口号为 40924
	host = "0.0.0.0"
	port = 40924
	printing = True
	connection = False

	def __init__(self, printing=True):
		self.printing = printing

	def connect(self, printing=True):  # 与机器人控制命令端口建立 UDP 连接
		self.address = (self.host, int(self.port))
		self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		if self.printing or printing:
			print("Connecting_UDP...")

		self.udp_socket.bind(self.address)

		if self.printing or printing:
			print("UDP_Connected!")

	def disconnect(self, printing=True):
		if self.printing or printing:
			print("UDP disconnecting...")
		self.udp_socket.close()
		if self.printing or printing:
			print("UDP disconnected!")

	def try_get(self, timeout=5,
	            printing=True):  # 这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。
		result = ''
		try:
			# 设置超时时间
			ready = select.select([self.udp_socket], [], [], timeout)
			# print(ready)
			if ready[0]:
				# 如果有可读数据，接收并解码
				# print("hearing...")
				buf = self.udp_socket.recv(1024)
				result = buf.decode('utf-8')
			else:
				result = 'no_OUT'

		except socket.error as e:
			if self.printing or printing:
				print("Error receiving :", e)

			sys.exit(1)

		if self.printing or printing:
			print(result)

		return result


class TCP_video:
	host = "192.168.42.2"
	port = 40921
	printing = True
	connection = False

	def __init__(self, printing=True):
		self.printing = printing

	def connect(self, printing=True):  # 与机器人控制命令端口建立 TCP 连接
		TCP_video.address = (TCP_video.host, int(TCP_video.port))
		self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.printing or printing:
			print("Connecting_TCP_video...")

		# self.TCP_socket.connect(self.address)
		print(self.address)
		try:
			self.TCP_socket.connect((self.host, int(TCP_video.port)))
		except Exception as e:
			print('Connection failed, the reason is %s' % e)
		self.connection = True
		if self.printing or printing:
			print("TCP_video_Connected!")

		self.cmd_socket_msg_queue = {
			self.TCP_socket: queue.Queue(32)
		}
		self.cmd_socket_recv_thread = threading.Thread(target=self.__socket_recv_task)
		self.cmd_socket_recv_thread.start()

	"""
        Receive control data

        If optional arg 'timeout' is None (the default), block if necessary until
        get data from control port. If 'timeout' is a non-negative number,
        it blocks at most 'timeout' seconds and reuturn None if no data back from
        robot video port within the time. Otherwise, return the data immediately.
 
        If optional arg 'latest_data' is set to True, it will return the latest
        data, instead of the data in queue tail.

        """

	def recv_video_data(self, timeout=None, latest_data=False):
		return self.__recv_data(self.TCP_socket, timeout, latest_data)

	def __recv_data(self, socket_obj, timeout, latest_data):
		msg = None
		try:
			msg = self.queue.Queue(32).get(timeout=timeout)
		except Exception as e:
			return None
		else:
			return msg

	def __socket_recv_task(self):
		while True:
			rlist, _, _ = select.select([self.TCP_socket], [], [], 2)
			for s in rlist:
				msg, addr = s.recvfrom(4096)
				if self.cmd_socket_msg_queue[s].full():
					self.cmd_socket_msg_queue[s].get()
				self.cmd_socket_msg_queue[s].put(msg)
