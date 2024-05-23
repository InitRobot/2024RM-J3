import cv2


class vidio:
	def __init__(self, cv2_):
		self.cap = cv2_.VideoCapture(1)
		print("set")
		self.fps = self.cap.get(cv2_.CAP_PROP_FPS)
		# fps=30
		self.size = (int(self.cap.get(cv2_.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2_.CAP_PROP_FRAME_HEIGHT)))
		# fps = cap.get(cv2.CAP_PROP_FPS)

	def get_vidio(self, printing=False):
		success, frame_ = self.cap.read()
		if not success:
			if printing:
				print("fail")
			return False
		return frame_


if __name__ == '__main__':
	my_vidio = vidio(cv2)
	while True:
		frame = my_vidio.get_vidio(printing=True)
		print(frame)
