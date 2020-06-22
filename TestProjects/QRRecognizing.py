import cv2, time

################################################################
path = 'cascade70N20S.xml'  # PATH OF THE CASCADE
cameraNo = 0  # CAMERA NUMBER
objectName = 'QR'  # OBJECT NAME TO DISPLAY
frameWidth = 640  # DISPLAY WIDTH
frameHeight = 480  # DISPLAY HEIGHT
color = (139,0,0)

img_counter = 0

cap = cv2.VideoCapture(cameraNo)
# cap = cv2.VideoCapture('rtsp://root:TO-41212@169.254.21  6.136/live.sdp')
cap.set(3, frameWidth)
cap.set(4, frameHeight)
ret, frame = cap.read()

def empty(a):
    pass

cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight + 100)

cascade = cv2.CascadeClassifier(path)

while True:
    # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
    cameraBrightness = 0
    cap.set(10, cameraBrightness)
    # GET CAMERA IMAGE AND CONVERT TO GRAYSCALE
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # DETECT THE OBJECT USING THE CASCADE
    scaleVal = 2
    neig = 19
    objects = cascade.detectMultiScale(gray, scaleVal, neig)
    # DISPLAY THE DETECTED OBJECTS
    for (x, y, w, h) in objects:

        area = w * h
        minArea = 20000
        if area > minArea:
            print("realcoordinates: ", x, y, w, h)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            cv2.putText(img, objectName, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            roi_color = img[y:y + h, x:x + w]





    cv2.imshow("Result", img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k%256 == 32 and qrexist: #take screenshot
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame[qry:qrh, qrx:qrw])
        # cv2.imwrite(img_name, frame[170:254, 458:446])
        print("{} written!".format(img_name))
        img_counter += 1

cap.release()
cv2.destroyAllWindows()