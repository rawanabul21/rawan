import cv2
import os

cap = cv2.VideoCapture('C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\videos\\test17g.MOV')
path = 'C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\output_screenshots\\test17g_frames'
i = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(os.path.join(path , str(i) + '.jpg'), frame)
    i += 1

cap.release()
cv2.destroyAllWindows()