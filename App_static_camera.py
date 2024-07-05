import cv2
 
if __name__ == '__main__' :

    tracker = cv2.TrackerKCF_create()

    video = cv2.VideoCapture(0)
 
    ok, frame = video.read()
     
    bbox = (287, 23, 86, 320)
 
    bbox = cv2.selectROI(frame, False)
 
    ok = tracker.init(frame, bbox)
 
    while True:
        ok, frame = video.read()
        if not ok:
            break
         
        timer = cv2.getTickCount()
        ok, bbox = tracker.update(frame)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        cv2.imshow("Tracking", frame)
 
        if (cv2.waitKey(1) & 0xff) == 27 : break