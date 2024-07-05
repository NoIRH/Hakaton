import cv2
import numpy as np

mask = None

is_init = True
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

cap = cv2.VideoCapture('test videos\C2024-04-08-14-01-50-01.mp4') # Замените 'video.mp4' на путь к вашему видео

ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

hsv = np.zeros_like(prev_frame)
hsv[..., 1] = 255

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    if is_init:
        x, y, w, h = cv2.selectROI(bgr, False)
        track_window = (x, y, w, h)

        roi = bgr[y:y+h, x:x+w]
        hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        is_init = False

    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist,[0,180],1)

    # apply camshift to get the new location
    ret, track_window = cv2.CamShift(dst, track_window, term_crit)

    # Draw it on image
    pts = cv2.boxPoints(ret)
    pts = np.int32(pts)
    img2 = cv2.polylines(bgr,[pts],True, 255,2)
    # cv2.imshow('img2',img2)


    cv2.imshow('Optical Flow', img2)
    
    prev_gray = gray

    if (cv2.waitKey(30) & 0xff) == 27:
        break

cap.release()
cv2.destroyAllWindows()
