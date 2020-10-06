import cv2
import numpy as np
from pyzbar.pyzbar import decode

#image = cv2.imread('C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\qr_test3.jpg')
#cap = cv2.VideoCapture(0)
def write_to_file(path, line1, line2):
    f = open("Data Collection\\qrcode\\qr_output.txt", "a+")
    f.write(path + "\n")
    for (i,j) in zip(line1, line2):
        f.write("Area: ")
        f.write(i + '\n')
        f.write("Location: ")
        f.write(j +'\n')

def individual_file(name, line1,line2):
    f = open('C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\qrcode\\' + name + '.txt', "a+")
    for (i,j) in zip(line1, line2):
        f.write("Area: ")
        f.write(i + '\n')
        f.write("Location: ")
        f.write(j +'\n')


name = "test47c"
path = 'C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\videos\\' + name + '.mov'


cap = cv2.VideoCapture(path)

#cap.set(3, 640)
#cap.set(4,480)
area = []
location = []
while cap.isOpened():
    success, frame = cap.read()
    if success == False or cv2.waitKey(1) == ord('q'):
        break
    #img = cv2.rotate(frame, cv2.ROTATE_180)
    #img = cv2.resize(img, (1392, 1024), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    img = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)

    for barcode in decode(img):
        #read and detect qr code
        myData = barcode.data.decode('utf-8')
        area.append(str(myData))
        location.append(str(barcode.rect))
        print(myData)
        print(barcode.rect)


        #draw bounding box around qrcode
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img, [pts], True, (0,255,0), 5)

        #display the qr code message on video
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,222), 2)


    cv2.imshow('Result', img)
    cv2.waitKey(1)
if area != []:
    write_to_file(path, area, location)
    individual_file(name, area, location)
cap.release()
cv2.destroyAllWindows()


