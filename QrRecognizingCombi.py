import cv2  # camera use and Recognize program
import pyzbar.pyzbar as pyzbar  # Recognize program
from webcolors import *  #
import pyodbc  # database connection


def defaultSettings() -> object:
    """
    Gives certain variables a value in case they aren't manually changed
    :rtype: object
    :return:
    """
    path = 'cascade70N20S.xml'  # cascade file
    object_name = 'QR'
    frame_width = 640
    frame_height = 480
    color = name_to_rgb('GREEN')
    camnum = 0  # Camera number
    return frame_width, frame_height, path, camnum, object_name, color


def notneeded(a):
    """
    Incase of empty/not used variabele still need to have a function/value
    :param a:
    :return:
    """
    pass


def databaseUsing(connectie, execute, insert, barcode, database_name, section_name):  # database connnection function
    """
    Makes it possible to connect to a database with the manually used values
    :rtype: object
    :param connectie: connectie code
    :param execute: execution code
    :param insert: 2d execution code
    :param barcode: barcode number
    """
    conn = pyodbc.connect(connectie)  # connection with database
    cursor = conn.cursor()  # get cursor
    # execute first command
    # ~
    barcodenumber = str(barcode, 'utf-8')
    # print('''IF NOT EXISTS
    # (SELECT 1 FROM ''' + database_name + ''' WHERE ''' + section_name + ''' = ' ''' + barcodenumber + '''')
    #
    # BEGIN ''' + insert + ''' VALUES ('0'''+ barcodenumber + '''' ) END''')

    cursor.execute('''IF NOT EXISTS 
    (SELECT 1 FROM ''' + database_name + ''' WHERE ''' + section_name + ''' = '0''' + barcodenumber + '''') 
    
    BEGIN ''' + insert + ''' VALUES ('0'''+ barcodenumber + '''') END''')
    # ~ Execute second command
    conn.commit()
    pass


def createRectangle(img, x, y, w, h, color, object_name):
    """
    Makes a rectangle with certain coordinates
    :rtype: object
    :param img: photo information
    :param x: coordinate
    :param y: coordinate
    :param w: coordinate
    :param h: coordinate
    :param color: chosen color
    :param object_name: chosen name to give object
    """
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)  # create rectangle
    cv2.putText(img, object_name, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)


def cascadeRunning(frame_width, frame_height, path, camnum, objectName, color, databaseUse, connectie, execute, insert, database_name, section_name):
    """
    Gives connection to (web)cam,
    checks if code is found,
    ask which entries are filled,
    uses functions for certain used entries,
    closes connection with (web)cam if esc pressed
    :rtype: object
    :param frame_width: frame width
    :param frame_height: frame height
    :param path: cascade file
    :param camnum: camera number
    :param objectName: chosen name to give object
    :param color: chosen color
    :param databaseUse: yes or no
    :param connectie: connectie code
    :param execute: execution SQL code
    :param insert: 2d execution SQL code
    """
    cap = cv2.VideoCapture(camnum)  # activates camera
    cap.set(3, frame_width)
    cap.set(4, frame_height)
    qrcodefound = False  # default on False
    cv2.resizeWindow("Result", frame_width, frame_height + 100)
    cascade = cv2.CascadeClassifier(path)
    try:
        while True:
            cap.set(10, 0)  # 2d value == Camera Brightness
            success, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Make non-visable readable Camera Color
            objects = cascade.detectMultiScale(gray, 2, 19)  # makes video gray to search better
            for (x, y, w, h) in objects:  # Display Live Objects (Beta)
                area = w * h
                minArea = 20000
                if area > minArea:  # If object has correct size
                    createRectangle(img, x, y, w, h, color, objectName)
            decodedObjects = pyzbar.decode(img)  # decodes barcodes out video
            for obj in decodedObjects:  # every barcodes it finds
                barcode = obj.data  # place it in a variable
                if databaseUse:  # if databaseUse is true
                    databaseUsing(connectie, execute, insert, barcode, database_name, section_name)  # use function datbase Using
                print("Data", barcode)  # print it in console
            if qrcodefound == False:
                cv2.imshow("Camera", img)
            k = cv2.waitKey(30) & 0xff  # wait until key pressed
            if k == 27:  # if ESC break loop
                break
    except cv2.error:
        print("Camera not connectable")

    cap.release()
    cv2.destroyAllWindows()
