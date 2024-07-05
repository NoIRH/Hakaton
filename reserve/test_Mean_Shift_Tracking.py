import cv2
import numpy as np

# Загрузка видео
cap = cv2.VideoCapture('test videos\C2024-04-08-14-00-37-01.mp4')

# Настройки Mean Shift Tracking
params = {
    'term_criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1),
    'roi_box': None
}

# Чтение первого кадра
ret, frame = cap.read()

print('select')

# Выбор области для отслеживания
params['roi_box'] = cv2.selectROI(frame, False)

print('good')

# Инициализация трекера
roi_hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Применение Mean Shift Tracking
    dst = cv2.calcBackProject([frame], [0], roi_hist, [0, 256], 1)
    ret, params['roi_box'] = cv2.CamShift(dst, params['roi_box'], params['term_criteria'])

    # Отрисовка прямоугольника вокруг объекта
    pts = cv2.boxPoints(ret)
    pts = np.int32(pts)
    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

    # Отображение кадра
    cv2.imshow('Mean Shift Tracking', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
