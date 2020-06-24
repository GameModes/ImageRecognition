import cv2
import pyzbar.pyzbar as pyzbar
from webcolors import *
import pyodbc



def defaultSettings():
    path = 'cascade70N20S.xml'  # PATH OF THE CASCADE
    objectName = 'QR'  # OBJECT NAME TO DISPLAY #{aanpasbaar}
    frameWidth = 640  # DISPLAY WIDTH #{aanpasbaar}
    frameHeight = 480  # DISPLAY HEIGHT #{aanpasbaar}
    color = name_to_rgb('GREEN') #{aanpasbaar}

    camnum = 0 #Camera nummer of IP {aanpasbaar}
    return frameWidth, frameHeight, path, camnum, objectName, color


def notneeded(a):
    pass


def databaseUsing(connectie, execute, insert, barcode):
    conn = pyodbc.connect(connectie)
    cursor = conn.cursor()
    cursor.execute(execute)
    #~
    cursor.execute('''IF NOT EXISTS (SELECT 1 FROM QRDatabase
    WHERE QRCode = ''' + str(barcode) + ''')''' +
    '''BEGIN''' + insert + '''VALUES (''' + barcode + ''') END''')
    #~
    conn.commit()
    pass


def cascadeRunning(frameWidth, frameHeight, path, camnum, objectName, color, databaseUse, connectie, execute, insert):

    cap = cv2.VideoCapture(camnum)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    qrcodefound = False
    cv2.namedWindow("Result")
    cv2.resizeWindow("Result", frameWidth, frameHeight + 100)
    cascade = cv2.CascadeClassifier(path)
    try:
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
            decodedObjects = pyzbar.decode(img)
            for obj in decodedObjects:
                barcode = obj.data
                if databaseUse:
                    databaseUsing(connectie, execute, insert, barcode)
                print("Data", barcode)

            if qrcodefound == False:
                cv2.imshow("Result", img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
    except cv2.error:
        print("Camera not connectable")

    cap.release()
    cv2.destroyAllWindows()
