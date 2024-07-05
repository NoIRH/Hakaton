import numpy as np
import cv2 as cv
 
cap = cv.VideoCapture('test videos\C2024-04-08-14-00-37-01.mp4') # Замените 'video.mp4' на путь к вашему видео

while True:
    ret, frame = cap.read()
    if not ret: 
        break

    
    # kernel = np.ones((5,5),np.uint8)
    # erosion = cv.erode(frame, kernel, iterations = 1)
    # dilatation = cv.dilate(erosion,kernel,iterations = 1)

    oper_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 
    oper_frame = np.float32(oper_frame) 
    oper_frame = cv.cornerHarris(oper_frame, 2, 5, 0.07)
    oper_frame = cv.dilate(oper_frame, None) 
    frame[oper_frame > 0.01 * oper_frame.max()] = [0, 0, 255] 
    frame[oper_frame < 0.01 * oper_frame.max()] = [0, 0, 0] 

    cv.imshow('dilatation', frame)

    if (cv.waitKey(30) & 0xff) == 27:
        break
cap.release()
cv.destroyAllWindows()
