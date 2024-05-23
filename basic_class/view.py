import cv2
import time

# 可以是网络推流地址 也可以是本地视频地址
cap = cv2.VideoCapture(1)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = cap.get(cv2.CAP_PROP_FPS)
# fps=30
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# size=(960,544)
i = 0
while (cap.isOpened()):
	i = i + 1
	ret, frame = cap.read()

	# 获取最新图片
	allcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
	cap.set(cv2.CAP_PROP_POS_FRAMES, allcount)

	# time.sleep(2)
	ss = cap.get(2)
	print(ss)
	if ret == True:
		print("in")
		# cv2.imshow('./image/' + str(i) + '.jpg', frame)
		# cv2.waitKey(1)
	else:
		break
cap.release()

cv2.destroyAllWindows()
