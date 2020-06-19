import cv2 as cv
import numpy as np


cap = cv.VideoCapture('rtsp://root:TO-41212@169.254.216.136/live.sdp')  # beeld van 640x360

upper_range = np.array([149, 255, 147], dtype="uint8") # 149, 198, 141
lower_range = np.array([47, 150, 24], dtype="uint8") # 47, 169, 24

while cap.isOpened():
    ret, frame = cap.read()
    img_crop = frame[250:900, 500:1500]# naar beneden, pixel hoogte beeld, naar rechts, pixel breedte beeld
    blur = cv.GaussianBlur(img_crop, (21,21), 0)
    detectie = cv.inRange(blur, lower_range, upper_range)




    counter = cv.countNonZero(detectie)
    print(counter)
    #cv.imshow('orgioneel', frame)
    cv.imshow('blur', blur)
    cv.imshow('orgioneel', img_crop)
    cv.imshow('detectie', detectie)

    if cv.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()