import cv2
import robomaster
from robomaster import robot
from ultralytics import YOLO
import re
import time

# 加载预训练的 YOLOv8 模型
model = YOLO('../../RM-yolo/runs/best.pt')


# 路径需修改

def connect():
	ep_robot = robot.Robot()
	ep_robot.initialize(conn_type="rndis")
	ep_gimbal = ep_robot.gimbal
	ep_blaster = ep_robot.blaster
	ep_camera = ep_robot.camera
	# ep_camera.start_video_stream(display=False, resolution='360p')


def disconnect():
	cv2.destroyAllWindows()
	ep_camera.stop_video_stream()
	ep_robot.close()


def auto_aim():
	img = ep_camera.read_cv2_image(strategy='newest')

	results = model(img)

	for r in results:
		boxes = r.boxes

	pos = boxes.xywh
	pos = str(pos)

	pos_arr = []
	pos_arr = re.findall("\d+\.?\d*", pos)

	print("↓\n")
	print(pos_arr)
	print("↑\n")

	annotated_frame = results[0].plot()
	cv2.imshow("YOLOv8", annotated_frame)

	posx = float(pos_arr[0]) + 40
	posy = float(pos_arr[1]) - 20

	if float(pos_arr[0]) != 0:
		yaw = int((posx / 360 - 1) * 55)
		pitch = -int((posy / 180 - 1) * 55)
		print(yaw, pitch)
		ep_gimbal.move(yaw=yaw, pitch=pitch, pitch_speed=20, yaw_speed=20)
		time.sleep(1)
		ep_blaster.fire()

	cv2.waitKey(1)
