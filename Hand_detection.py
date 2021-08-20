import cv2
import mediapipe as mp
import time
import time
import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.mediapipe.python.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,
                                        self.detectionCon,
                                        self.trackCon)

        self.mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img


    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)

                self.lmList.append([id, cx, cy])
                # if id == 4:
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return self.lmList


    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers


def main():
    # Volume control using hands
    # Using this we can control the volume using our hand
    # This project uses a previously created HAND TRACKING MODULE



    # Predefined variables for height and width
    wCam = 1000
    hCam = 600


    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    detector = handDetector(detectionCon=0.75)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # This is the volume range
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
    vol = 0
    volBar = 400
    volPer = 0

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if lmList:
            # print(lmList[4], lmList[8])
            # Index 4 represents the tip of the thumb (THUMB_TIP)
            # Index 8 represents the tip of the index finger (INDEX_FINGER_TIP)

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2-x1, y2-y1)
            # print(length)

            ''' 
            In my case:
            Hand range (length) is from 35 to 270
            Volume range is from -63.5 to 0
            These values could vary
            '''

            vol = np.interp(length, [35, 270], [minVol, maxVol])
            # print(int(length), vol)
            volBar = np.interp(length, [35, 270], [400, 150])
            volPer = np.interp(length, [35, 270], [0, 100])

            volume.SetMasterVolumeLevel(vol, None)

            if length <= 35:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0, 255, 0), 2)

        cTime = time.time()
        fps = int(1/(cTime-pTime))
        pTime = cTime
        cv2.putText(img, f'FPS: {fps}', (10, 30),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

        cv2.imshow('IMAGE', img)
        cv2.waitKey(1)

if __name__=='__main__':
    main()