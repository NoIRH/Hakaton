import cv2
import numpy as np
from ultralytics import YOLO
import torch
from ultralytics.utils.plotting import Annotator, colors

from collections import defaultdict

print(torch.cuda.is_available())

track_history = defaultdict(lambda: [])
model = YOLO("yolov8x.pt")
names = model.model.names

video_path = "test\C2024-05-15-16-41-30-04.mp4"
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error reading video file"


cap = cv2.VideoCapture(video_path)
success, frame = cap.read()
prvs = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame)
hsv[...,1] = 255
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

def intersect(rect, point):
    if (point[0] >=rect[0] and point[0]  <= rect[2] and point[1]  >= rect[1] and point[1] <= rect[3]):
        return True
    else:
        return False
    
# def intersect(rect, point):
#     p1, p2, p3, p4 = map(Point, [(rect[0], rect[1])q, (rect[0] + rect[2], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (rect[0], rect[1] + rect[3])])
#     p5 = Point(point[0], point[1]) 
#     poly1 = Polygon(p1, p2, p3, p4)
#     print(p5)
#     print(poly1)
#     isIntersection = poly1.are_similar()
#     print(isIntersection)
    
#     if (point[0] >= rect[0] and point[0] <= rect[2] and point[1] >= rect[1] and point[1] <= rect[3]):
#         return True
#     else:
#         return False

while cap.isOpened():
    success, frame = cap.read()

    frame2  = cv2.GaussianBlur(frame,(21,21),0)
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.1, 4, 10, 2, 3, 1.0, 1)
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(bgr , cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 55, 200, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if success:
        results = model.track(frame, persist=True, verbose=False)
        boxes = results[0].boxes.xyxy.cpu()

        if results[0].boxes.id is not None:

            clss = results[0].boxes.cls.cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confs = results[0].boxes.conf.float().cpu().tolist()

            annotator = Annotator(frame, line_width=2)
            
            for box, cls, track_id in zip(boxes, clss, track_ids):
                is_box = False
                for  c in contours:
                    for p in c:
                        if intersect(box.numpy(),p[0]):
                            is_box = True
                if is_box:
                    annotator.box_label(box, color=colors(int(cls), True), label=names[int(cls)])

                track = track_history[track_id]
                track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
                if len(track) > 30:
                    track.pop(0)

                points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
                cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)

        cv2.imshow("YOLOv9 Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()