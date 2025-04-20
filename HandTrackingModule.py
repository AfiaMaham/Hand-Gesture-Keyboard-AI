import cv2 as cv
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplex=1,minCon=0.5,tracon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplex
        self.minCon = minCon
        self.tracon = tracon
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hand = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex,self.minCon,self.tracon)

    def findHand(self,img,draw=True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.result = self.hand.process(imgRGB)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo = 0,draw=True):
        lmsList = []
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handNo]
            for id,lms in enumerate(myhand.landmark):
                h,w,c = img.shape
                cx,cy = int(lms.x*w), int(lms.y*h)
                lmsList.append([id, cx, cy])
                if draw:
                    cv.circle(img,(cx,cy),15,(0,0,255),cv.FILLED)
        return lmsList



def main():
    ctime = 0
    ptime = 0
    lmList = []
    cap = cv.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHand(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[0])
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(img,str(int(fps)),(30,40),cv.FONT_HERSHEY_SIMPLEX,2,(0,255,0),5)

        cv.imshow("Camera", img)
        if cv.waitKey(1) & 0xff == ord("a"):
            break

if __name__ == "__main__":
    main()