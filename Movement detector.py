import cv2
import numpy as np
import time
from datetime import datetime
           
cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')

recor = cv2.VideoWriter('recorder.mp4', fourcc, 40, (640, 480))  # saves recorded file in .mp4 format with 640x480 quality and 40 speed

ret, frame1 = cap.read()
ret, frame2 = cap.read()


while True:
    dtime = datetime.now().strftime("Sana: %d-%m-%Y Soat: %H:%M")
    
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh, None, iterations=3)
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) > 600: # checks sensitivity of moving object
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2) # puts square on moving object
            cv2.putText(frame1, "Harakat aniqlandi!!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)
            cv2.putText(frame1, dtime, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)
            recor.write(frame1)
        else:
            continue
        
    cv2.imshow("Camera", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    key = cv2.waitKey(1)

    if key == 27:  #program exits when Esc button pressed
        break

recor.release()
cap.release()
cv2.destroyAllWindows()
    
    

    
