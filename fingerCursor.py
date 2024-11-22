import cv2
import mediapipe as mp
import HandTmodule as ht
import time
import numpy as np
import math
import pyautogui
import mouse



cap = cv2.VideoCapture(0)
wCam = 960
hCam = 540
cx,cy = 960//2, 540//2
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
detector = ht.hDetector(detectConf=0.7)
rectCol = (255,0,0)
size = pyautogui.size()
cenCol = (255,255,0)
clicking = False
lastime = time.time()
prev_cursor = [0, 0]
alpha = 0.5
buffer = []
smoothCoeff = 7
while True:
	succ, img = cap.read()
	img = cv2.flip(img, 1)
	img = detector.find(img, draw=False)
	lmLis = detector.findPos(img, point=[4,8,6])
	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime
	if len(lmLis) > 0:
		cursor = lmLis[8]
		distance = math.hypot((lmLis[4][1]-lmLis[6][1]), (lmLis[4][2]-lmLis[6][2]))
		
					
		cv2.line(img, lmLis[4][1:], lmLis[6][1:], (255, 255, 0), 2, 2)
		cv2.circle(img, (((lmLis[4][1]+lmLis[6][1])//2),((lmLis[4][2]+lmLis[6][2])//2)), 10, cenCol, cv2.FILLED)
		if (cx-(wCam//3))<cursor[1]<(cx+(wCam//3)) and (cy-(hCam//3))<cursor[2]<(cy+(hCam//3)):
			cursor[1] = np.interp(cursor[1], [(cx-(wCam//4)),cx+(wCam//4)], [0, size[0]])
			cursor[2] = np.interp(cursor[2], [(cy-(hCam//4)),cy+(hCam//4)], [0, size[1]])
			currX = prev_cursor[0]+((cursor[1]-prev_cursor[0])//smoothCoeff)
			currY = prev_cursor[1]+((cursor[2]-prev_cursor[1])//smoothCoeff)
			# print([currX,currY])
			mouse.move(currX, currY)
			prev_cursor = [currX,currY]
			rectCol = (0,0,255)

			if distance < 40:
				clicking = True
				lastime = time.time()
				cenCol = (0,255,255)
				# mouse.drag()
			else:
				if clicking:
					if time.time() - lastime < 1:
						mouse.click('left')
				clicking = False
				cenCol = (255,255,0)

			xDist = math.hypot((prev_cursor[0]-cursor[1]),(prev_cursor[1]-cursor[2]))
			# if len(buffer) == 3:
			# 	xAvg = np.array([x[0] for x in buffer])
			# 	yAvg = np.array([x[1] for x in buffer])
			# 	mouse.move(np.mean(xAvg),np.mean(yAvg), True, duration=1)
			# 	buffer = []
			# else:
			# 	buffer.append([cursor[1],cursor[2]])
		else:
			rectCol = (255,0,0)
	cv2.rectangle(img, (cx-(wCam//4),cy-(hCam//4)), (cx+(wCam//4),cy+(hCam//4)), rectCol, 2, 3)
	cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


	cv2.imshow("image",img)
	cv2.waitKey(10)