#importing all packages

import cvzone
import numpy as np
import pyfirmata
import cv2
from cvzone.HandTrackingModule import HandDetector

#iniciating capture

Capture = cv2.VideoCapture(0)

#window size
w, h = 640, 480
Capture.set(3, w)
Capture.set(4, h)

if not Capture.isOpened():
    print("Camera is not opened, either camera is disabled or wrong index is inputed")

#connecting to arduino
port = 'COM3'
board = pyfirmata.Arduino(port)
servo_pinX = board.get_pin('d:9:s') #digital pin 9 in arduino
servo_pinY = board.get_pin('d:10:s') #digital pin 10 in arduino

#initialize hand detector form cvzone module
detector = HandDetector(maxHands=2, detectionCon=0.8)

while Capture.isOpened():
    success, frame = Capture.read() #reads the frame form camrea
    hands, frame = detector.findHands(frame) #reads hands from camera
    for hand in hands:
        #getting index finger tip coodinates
        px, py = hand['lmList'][8][0], hand['lmList'][8][1]

        #converting px and py to servo degrees
        servoX = int(np.interp(px, [0, w], [180, 0]))
        servoY = int(np.interp(py, [0, h], [0, 180]))

        #display servo positions on the created window
        cv2.putText(frame, f'Servo X: {servoX} Y: {servoY}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)

        #sending the servo position instructions to arduino
        servo_pinX.write(servoX)
        servo_pinY.write(servoY)

    #displaying the window
    cv2.imshow('Servo Hand Tracking', frame)

    #wait interval and exit condition
    key = cv2.waitKey(1)
    if key == ord('1'):
        break
#exit program
Capture.release()
cv2.destroyAllWindows()
exit()

