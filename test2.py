import cv2

import test as reader
path = 'C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\videos\\qrtest10.mov'

cap = cv2.VideoCapture(path)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    codes, frame = reader.extract(frame, True)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("I quit!")
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()