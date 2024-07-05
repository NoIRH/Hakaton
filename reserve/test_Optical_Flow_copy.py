import cv2
import numpy as np

cap = cv2.VideoCapture('test videos\C2024-04-08-14-00-37-01.mp4') # Замените 'video.mp4' на путь к вашему видео

L_limit=np.array([0,0,45]) 
U_limit=np.array([255,255,255])

ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

hsv = np.zeros_like(prev_frame)
hsv[..., 1] = 255

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.GaussianBlur(gray,(5,5),0)

    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 1, 10, 3, 5, 1.2, 0)
    


    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] =  0 #ang * 180 / np.pi / 2

    # mag[mag >  0.5 * mag.max()] = 255
    mag[mag <  0.7 * mag.max()] = 0

    hsv[..., 2] =  cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)


    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
 

    сontours, _ = cv2.findContours(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY) , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # нахождение массива контурных точек
 
   


    for contour in сontours:
            (x, y, w, h) = cv2.boundingRect(contour) # преобразование массива из предыдущего этапа в кортеж из четырех координат
        
        #     # метод contourArea() по заданным contour точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в каждый момент времени, это можно проверить
            # print(cv.contourArea(contour))
        
            if cv2.contourArea(contour) < 200: # условие при котором площадь выделенного объекта меньше 700 px
                continue
            cv2.rectangle(bgr, (x, y), (x+w, y+h), (0, 255, 0), 2) # получение прямоугольника из точек кортежа
        #     # cv2.putText(frame1, "Status: {}".format("Dvigenie"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA) # вставляем текст
        
            cv2.drawContours(bgr, contour, -1, (0, 255, 0), 2) #также можно было просто нарисовать контур объекта

    cv2.imshow('Optical Flow', bgr)
    
    prev_gray = gray

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
