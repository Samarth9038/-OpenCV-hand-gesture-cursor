import cv2
import mediapipe as mp
import time
import numpy as np


class hDetector():
    def __init__(self, mode=False, maxHands=1, detectConf=0.5, tracConf=0.5, modelComp = 1):
        self.mode = mode
        self.maxHand = maxHands
        self.detectConf = detectConf
        self.tracConf = tracConf
        self.modelComp=  modelComp

        self.pHands = mp.solutions.hands
        self.hands = self.pHands.Hands(self.mode, self.maxHand, self.modelComp, self.detectConf, self.tracConf)
        self.mDraw = mp.solutions.drawing_utils

    def find(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.hands.process(imgRGB)


        if self.res.multi_hand_landmarks:
            for handLms in self.res.multi_hand_landmarks:
                    if draw:
                        self.mDraw.draw_landmarks(img,handLms, self.pHands.HAND_CONNECTIONS)
        return img

    def findPos(self, img, draw=True, point=[0]):
        lmLisH1 = []
        if self.res.multi_hand_landmarks:
            selHand1 = self.res.multi_hand_landmarks[0]
            for id, lms in enumerate(selHand1.landmark):
                        h,w,c = img.shape
                        cx, cy = int(lms.x*w), int(lms.y*h)
                        lmLisH1.append([id, cx, cy])
            if draw:
                if len(lmLisH1) != 0:
                    [cv2.circle(img, lmLisH1[dot][1:], 10, (255,0,255), cv2.FILLED) for dot in point]
                # if len(lmLisH2) != 0:
                #     [cv2.circle(img, lmLisH2[dot][1:], 10, (0,255,255), cv2.FILLED) for dot in point]
        return lmLisH1



def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = hDetector(detectConf=0.7)
    while True:
        succ, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.find(img)
        lmLis = detector.findPos(img, draw=False)
        if len(lmLis) != 0:
             print(lmLis[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("image",img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()