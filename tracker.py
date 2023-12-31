import cv2
import mediapipe as mp
import time
import psutil
from AppOpener import open, close

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        lmList = []
        for handLms in results.multi_hand_landmarks:
            for id, lm, in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                # print(lmList)
            if len(lmList) != 0:
                if lmList[8][2] < lmList[6][2]:
                    if "notepad.exe" in (i.name() for i in psutil.process_iter()):
                        continue
                    else:
                        open("notepad")
                else:
                    close("notepad")
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # shows fps
    # cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)

    cv2.imshow("Video", img)
    cv2.waitKey(1)
