import cv2 #camera use and Recognize program
import pyzbar.pyzbar as pyzbar #Recognize program
from webcolors import * #
import pyodbc  #database connection

def defaultSettings():
    path = 'cascade70N20S.xml'  # cascade file
    objectName = 'QR'
    frameWidth = 640
    frameHeight = 480
    color = name_to_rgb('GREEN')
    camnum = 0 #Camera number
    return frameWidth, frameHeight, path, camnum, objectName, color


def notneeded(a): #notneeded functie if neeed
    pass


def databaseUsing(connectie, execute, insert, barcode): #database connnection function
    conn = pyodbc.connect(connectie) #connection with database
    cursor = conn.cursor() #get cursor
    cursor.execute(execute) #execute first command
    #~
    cursor.execute('''IF NOT EXISTS (SELECT 1 FROM QRDatabase
    WHERE QRCode = ''' + str(barcode) + ''')''' +
    '''BEGIN''' + insert + '''VALUES (''' + barcode + ''') END''')
    #~ Execute second command
    conn.commit()
    pass


def cascadeRunning(frameWidth, frameHeight, path, camnum, objectName, color, databaseUse, connectie, execute, insert):
    cap = cv2.VideoCapture(camnum) #activates camera
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    qrcodefound = False  #default on False
    cv2.namedWindow("Camera")
    cv2.resizeWindow("Camera", frameWidth, frameHeight + 100)
    cascade = cv2.CascadeClassifier(path)
    try:
        while True:
            cap.set(10, 0) #2d value == Camera Brightness
            success, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Make non-visable readable Camera Color
            objects = cascade.detectMultiScale(gray, 2, 19) #makes video gray to search better
            for (x, y, w, h) in objects: # Display Live Objects (Beta)
                area = w * h
                minArea = 20000
                if area > minArea: #If object has correct size
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 3) #create rectangle
                    cv2.putText(img, objectName, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            decodedObjects = pyzbar.decode(img) #decodes barcodes out video
            for obj in decodedObjects: #every barcodes it finds
                barcode = obj.data #place it in a variable
                if databaseUse: #if databaseUse is true
                    databaseUsing(connectie, execute, insert, barcode) #use function datbase Using
                print("Data", barcode) #print it in console
            if qrcodefound == False:
                cv2.imshow("Result", img)
            k = cv2.waitKey(30) & 0xff #wait until key pressed
            if k == 27: #if ESC break loop
                break
    except cv2.error:
        print("Camera not connectable")

    cap.release()
    cv2.destroyAllWindows()
