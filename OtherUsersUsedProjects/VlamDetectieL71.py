import cv2 as cv
import numpy as np
from datetime import timedelta
from datetime import datetime
#import RPi.GPIO as GPIO
memtijd = 0
fotogemaakt = 0

cap = cv.VideoCapture('rtsp://10.136.108.203/live.sdp') # beeld van 1920x1080

upper_range = np.array([255,255,255], dtype="uint8")
lower_range = np.array([230,230,230], dtype="uint8")

while cap.isOpened():
    ret, orgioneel = cap.read()
    img_interest = orgioneel[250:400, 50:300]
    blurred_frame = cv.GaussianBlur(img_interest, (7,7),0)
    mask = cv.inRange(blurred_frame, lower_range, upper_range)


    #cv.imshow('orgioneel', orgioneel)
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    aantal = 0
    # kijken hoe groot de vlammen zijn
    for contour in contours:
        if cv.contourArea(contour) > 200:
            aantal += 1
            #print('aantal: ' + str(aantal) + ', pixels: ' + str(cv.contourArea(contour)))
            cv.drawContours(img_interest, contour, -1, (255, 0, 0), 1)


    #print('aantal: ' + str(aantal))

    cv.putText(img_interest, str(aantal), (20,40), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))

    cv.imshow('img_interest', img_interest)
    cv.imshow('mask', mask)

    dt = datetime.now()

    if (aantal < 4) and (aantal > 1):
        elapsed = ((dt.minute * 60) + dt.second) - memtijd
        #print('tijdsverschil: ' + str(elapsed))
        if int(elapsed) > 2 and fotogemaakt != dt.minute:
            cv.imwrite(str(dt.day) + ' ' + str(dt.hour) + '_' + str(dt.minute) + '.jpg', orgioneel)
            cv.imwrite(str(dt.day) + ' ' + str(dt.hour) + '_' + str(dt.minute) + ' filter.jpg', mask)
            fotogemaakt = dt.minute
            print('afbeelding ' + str(dt.day) + ' ' + str(dt.hour) + '_' + str(dt.minute) + '.jpg' + ' weg geschreven')
    else:
        memtijd = ((dt.minute * 60) + dt.second)

    # 50 ms wachten: dit scheelt CPU tijd
    #cv.waitKey(50)
    #print('einde bericht')


    if cv.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
