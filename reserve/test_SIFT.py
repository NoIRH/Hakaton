import cv2 
sift = cv2.xfeatures2d.SIFT_create() 
  
# Reading the image and converting into B/W 
cap = cv2.VideoCapture('test videos\C2024-04-08-14-01-50-01.mp4')

while True:
    ret, frame = cap.read()
    # image = cv2.imread('1.png') 
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    # Applying the function 
    kp, des = sift.detectAndCompute(gray_image, None) 
    
   
    # Applying the function 
    kp_image = cv2.drawKeypoints(frame, kp, None, color=(0, 255, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 
    cv2.imshow('SIFT', kp_image) 
    if (cv2.waitKey(30) & 0xff) == 27:
            break

cap.release()
cv2.destroyAllWindows()