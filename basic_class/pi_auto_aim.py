import get_view
import re
from ultralytics import YOLO
import cv2


class aim:
	model = YOLO('../../RM-yolo/runs/best.pt')

	def __init__(self):
		self.vidio = get_view.vidio(cv2)

	def target(self, blue):
		if blue:
			pass
		else:
			img = self.vidio.get_vidio(printing=True)
			results = self.model(img)
			for r in results:
				boxes = r.boxes
			pos = boxes.xywh
			pos = str(pos)
			pos_arr = re.findall("\d+\.?\d*", pos)
			print(pos_arr)


if __name__ == '__main__':
	a = aim()
	while True:
		a.target(False)
		print("1")
