import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from webcolors import *

def defaultSettings():
    path = 'cascade70N20S.xml'  # PATH OF THE CASCADE
    objectName = 'QR'  # OBJECT NAME TO DISPLAY #{aanpasbaar}
    frameWidth = 640  # DISPLAY WIDTH #{aanpasbaar}
    frameHeight = 480  # DISPLAY HEIGHT #{aanpasbaar}
    color = name_to_rgb('GREEN') #{aanpasbaar}

    camnum = 0 #Camera nummer of IP {aanpasbaar}
    # cap = cv2.VideoCapture('rtsp://root:TO-41212@169.254.216.136/live.sdp')
    return frameWidth, frameHeight, path, camnum, objectName, color


def notneeded(a):
    pass

def cascadeRunning(frameWidth, frameHeight, path, camnum, objectName, color):
    cap = cv2.VideoCapture(camnum)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    qrcodefound = False
    cv2.namedWindow("Result")
    cv2.resizeWindow("Result", frameWidth, frameHeight + 100)
    cascade = cv2.CascadeClassifier(path)
    while True:
        cap.set(10, 0) #2d value == Camera Brightness
        success, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Make non-visable readable Camera Color
        objects = cascade.detectMultiScale(gray, 2, 19)
        for (x, y, w, h) in objects: # Display Live Objects (Beta)
            area = w * h
            minArea = 20000
            if area > minArea: #If object has correct size
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3) #create rectangle
                cv2.putText(img, objectName, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
                roi_color = img[y:y + h, x:x + w]
                # qrcodefound = True
                # cropped = img[y:y + h, x:x + w, + h]
                # cv2.imshow("cropped", cropped)
        decodedObjects = pyzbar.decode(img)
        for obj in decodedObjects:
            print("Data", obj.data)

        if qrcodefound == False:
            cv2.imshow("Result", img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# frameWidth, frameHeight, path, cap, objectName, color = defaultSettings()
# cascadeRunning(frameWidth, frameHeight, path, cap, objectName, color)