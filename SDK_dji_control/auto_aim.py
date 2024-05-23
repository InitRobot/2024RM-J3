import cv2
from ultralytics import YOLO
import re
import time

model = YOLO('../../RM-yolo/runs/best.pt')


def auto_aim(img):
	# print("auto_aiming")
	results = model(img)
	for r in results:
		boxes = r.boxes
	pos = boxes.xywh
	pos = str(pos)
	pos_arr = []
	pos_arr = re.findall("\d+\.?\d*", pos)
	# print("↓\n")
	# print(pos_arr)
	# print("↑\n")

	annotated_frame = results[0].plot()
	cv2.imshow("YOLOv8", annotated_frame)
	cv2.waitKey(1)
	return pos_arr
