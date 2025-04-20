import cv2 as cv
import HandTrackingModule as htm
from time import sleep
from spellchecker import SpellChecker

def draw(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        if button.text == " ":
            cv.rectangle(img, button.pos, (x + w+20, y + h), (0, 0, 100), cv.FILLED)
        else:
            cv.rectangle(img,button.pos,(x+w,y+h),(0,0,100),cv.FILLED)
        cv.putText(img,button.text,(x+15,y+35),cv.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),4)
    return img

class Button():
    def __init__(self,pos,text,size = (55,55)):
        self.pos = pos
        self.text = text
        self.size = size

def hover(img,button_pos,button_text,size=(55,55)):
    x, y = button_pos
    w, h = size
    if button_text == " ":
        cv.rectangle(img, button_pos, (x + w + 20, y + h), (0, 0, 200), cv.FILLED)
        cv.putText(img, button_text, (x + 15, y + 35), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)

    cv.rectangle(img, button_pos, (x + w, y + h), (0, 0, 200), cv.FILLED)
    cv.putText(img, button_text, (x + 15, y + 35), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)




alpha = [["Q","W","E","R","T","Y","U","I","O","P"],
         ["A","S","D","F","G","H","J","K","L"],
         ["Z","X","C","V","B","N","M", " "]]

x = 0
buttonList = []

for i in range(len(alpha)):
    for j in range(len(alpha[i])):
        buttonList.append(Button((70*j+50+x, 70*i+150),alpha[i][j]))
    x += 20


cap = cv.VideoCapture(0)
cap.set(2,900)
cap.set(3,1300)
detector = htm.handDetector()
text = ""
checker = SpellChecker()
arr = []
corrWord = ""
typedText = ""

while True:
    success , img = cap.read()
    img = detector.findHand(img)
    img = draw(img, buttonList)

    lmList = detector.findPosition(img,draw=False)
    ind_x, ind_y = 0,0



    if lmList:
        ind_x, ind_y = lmList[8][1], lmList[8][2]

        cv.circle(img,(ind_x,ind_y),15,(0,100,0),cv.FILLED)

        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if x<ind_x<x+w and y<ind_y<y+h:
                hover(img,button.pos,button.text,button.size)


                if lmList[4][1] < lmList[8][1]:
                    if button.text == " ":
                        cv.rectangle(img, button.pos, (x + w + 20, y + h), (0, 100, 0), cv.FILLED)
                        cv.putText(img, button.text, (x + 15, y + 35), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)

                    cv.rectangle(img, button.pos, (x + w, y + h), (0, 100, 0), cv.FILLED)
                    cv.putText(img, button.text, (x + 15, y + 35), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)
                    sleep(0.8)

                    typedText = button.text
                    text += button.text
                    if text != " " and button.text == " ":
                        arr = text.split()
                        corrWord = checker.correction(arr[-1])

    if text != " ":
        if typedText == " " and len(corrWord) != "" and corrWord != arr[-1]:
            cv.rectangle(img, (195, 88), (260, 127), (0, 0, 100), cv.FILLED)
            cv.putText(img, f"Yes  Did you means '{corrWord.upper()}' ?", (200, 116), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)
        if (ind_x >= 195 and ind_y >= 90) and (ind_x <= 260 and ind_y <= 125):
            cv.rectangle(img, (195, 88), (260, 127), (0, 0, 200), cv.FILLED)
            cv.putText(img, f"Yes  Did you means '{corrWord.upper()}' ?", (200, 116), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)

            if lmList[4][1] < lmList[8][1]:
                cv.rectangle(img, (195, 88), (260, 127), (0, 100, 0), cv.FILLED)
                cv.putText(img, f"Yes  Did you means '{corrWord.upper()}' ?", (200, 116), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)

                arr[-1] = corrWord.upper()
                text = (" ".join(arr)) + " "

    cv.rectangle(img, (70, 40), (700, 80), (0, 0, 50), cv.FILLED)
    cv.putText(img, text, (80, 70 ), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 4)



    cv.imshow("keyboard", img)
    if cv.waitKey(1) & 0xff == ord("a"):
        break