#!python3

import sys

sys.path.append('../decoder/ubuntu/output/')
sys.path.append('../../connection/network/')

import threading
import time
import numpy as np
import libh264decoder
import signal
from PIL import Image as PImage
import cv2
import opus_decoder
import pyaudio
import robot_connection
import enum
import queue
import connect


class RobotLiveview(object):
	USB_DIRECT_IP = '192.168.42.2'

	def __init__(self, TCP):
		self.connection = TCP

		self.video_decoder = libh264decoder.H264Decoder()
		libh264decoder.disable_logging()

		self.video_decoder_thread = threading.Thread(target=self._video_decoder_task)
		self.video_decoder_msg_queue = queue.Queue(64)
		self.video_display_thread = threading.Thread(target=self._video_display_task)

		self.command_ack_list = []

		self.is_shutdown = False

	def display(self, TCP):
		self.command('command;', TCP)
		time.sleep(1)
		self.command('stream on;', TCP)
		time.sleep(1)
		self.command('stream on;', TCP)  # 以上连接并开启了视频流获取

		self.video_decoder_thread.start()  # 开启两个线程
		self.video_display_thread.start()

		print('display!')

	def command(self, msg, TCP):
		TCP.IN_OUT(msg)

	def _h264_decode(self, packet_data):  # 主要在这里decode   <----
		res_frame_list = []
		frames = self.video_decoder.decode(packet_data)
		for framedata in frames:
			(frame, w, h, ls) = framedata
			if frame is not None:
				frame = np.fromstring(frame, dtype=np.ubyte, count=len(frame), sep='')
				frame = (frame.reshape((h, int(ls / 3), 3)))
				frame = frame[:, :w, :]
				res_frame_list.append(frame)

		return res_frame_list

	def _video_decoder_task(self):  # decode线程
		package_data = b''

		while not self.is_shutdown:
			# print("try")
			buff = self.connection.recv_video_data()
			# print(buff)
			if buff:
				print("1")
				package_data += buff
				if len(buff) != 1460:
					for frame in self._h264_decode(package_data):
						try:
							self.video_decoder_msg_queue.put(frame, timeout=1)
						except Exception as e:
							if self.is_shutdown:
								break
							print('video decoder queue full')
							continue
						if self.video_decoder_msg_queue.qsize() >= 3:
							self.video_decoder_msg_queue.get(timeout=1)
						print("queuesize:", self.video_decoder_msg_queue.qsize())
					package_data = b''
		# print("end")

	def _video_display_task(self):  # display线程
		while not self.is_shutdown:
			try:
				frame = self.video_decoder_msg_queue.get(timeout=1)
			except Exception as e:
				if self.is_shutdown:
					break
				print('video decoder queue empty')
				continue
			image = PImage.fromarray(frame)
			img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
			cv2.imshow("Liveview", img)
			cv2.waitKey(1)
