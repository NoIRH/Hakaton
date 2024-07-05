import os
from pathlib import Path
import cv2
import numpy as np

def vidio_cupture(file,video_path ):
    # video_path = "C:\\MyApps\\video_cupturer_django\\video_cupturer_web\\media\\C2024-04-08-14-00-37-01.mp4"
    print(os.path.dirname(os.path.abspath(file))+video_path)
    print(video_path)
    video_path =os.path.dirname(os.path.abspath(file))+video_path
    output_path = os.path.dirname(os.path.abspath(file)) + "\media\output\\" + Path(file).stem + ".avi"
    cap = cv2.VideoCapture(Path(video_path).resolve())
    print(output_path)
    assert cap.isOpened(), "Error reading video file"

    cap = cv2.VideoCapture(video_path)

    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (w, h)) 

    L_limit=np.array([0,0,45])
    U_limit=np.array([255,255,255])

    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    hsv = np.zeros_like(prev_frame)
    hsv[..., 1] = 255

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 1, 10, 3, 5, 1.2, 0)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.1, 4, 10, 2, 3, 1.0, 1)
        
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        img_mask  = cv2.inRange(bgr, L_limit, U_limit)

        сontours, _ = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in сontours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 500:
                continue
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 2)
        
        output.write(frame)
        
        prev_gray = gray

    cap.release()
    output.release()
    cv2.destroyAllWindows()
    print('end')
    return Path(file).stem + ".avi"
