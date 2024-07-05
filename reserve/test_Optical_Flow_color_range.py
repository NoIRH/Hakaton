import cv2
import numpy as np

cap = cv2.VideoCapture('test videos\C2024-04-08-14-01-50-01.mp4')

ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

hsv = np.zeros_like(prev_frame)
hsv[..., 1] = 255

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(frame, kernel, iterations = 1)
    frame = cv2.dilate(erosion,kernel,iterations = 1)

    oper_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    oper_frame = np.float32(oper_frame) 
    oper_frame = cv2.cornerHarris(oper_frame, 2, 5, 0.07)
    oper_frame = cv2.dilate(oper_frame, None) 
    frame[oper_frame > 0.01 * oper_frame.max()]=[0, 0, 255] 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    


    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    
    # print(hsv)

    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    cv2.imshow('Optical Flow', bgr)
    
    prev_gray = gray

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
