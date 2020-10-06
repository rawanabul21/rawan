from __future__ import print_function
import cv2
import pytesseract
import os
import numpy as np
import copy
from google.cloud import vision
import os
import io
import cv2


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Rawan\\OneDrive\\Documents\\University\\Thesis\\key.json"

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

start = [51, '1600828825489']
end = [749, '1600828837109']
filepath = 'Data Collection\\output_screenshots\\test14a_frames'


def write_to_file(header, line1, line2):
    f = open("ocr_output.txt", "a+")
    f.write(header +"\n")
    f.write("Before Renaming: ")
    f.write(str(line1) +"\n")
    f.write("After Renaming: ")
    f.write(str(line2) +"\n")

#preprocess image to get better ocr reading
def preprocess(img):
    # preprocessing image
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = crop_bottom_half(img)

    # Make HSV and extract S, i.e. Saturation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]

    # Make greyscale version and inverted, thresholded greyscale version
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, grinv = cv2.threshold(gr, 127, 255, cv2.THRESH_BINARY_INV)

    # Find row numbers of rows with colour in them
    meanSatByRow = np.mean(s, axis=1)
    rows = np.where(meanSatByRow > 50)

    # Replace selected rows with those from the inverted, thresholded image
    gr[rows] = grinv[rows]
    img = gr

    cv2.medianBlur(img, 5)
    cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 5), np.uint8)
    cv2.dilate(img, kernel, iterations=1)
    kernel = np.ones((5, 5), np.uint8)
    cv2.erode(img, kernel, iterations=1)
    kernel = np.ones((5, 5), np.uint8)
    cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.Canny(img, 100, 200)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, sharpen_kernel)

    # resizing image
    scale_percent = 150
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dsize = (width, height)
    img = cv2.resize(img, dsize)

    cv2.imwrite("ocr_test\\" + filename, img)
    return img

#crop out the bottom half of the images for better ocr reading
def crop_bottom_half(image):
    cropped_img = image[0 :int(image.shape[0]/3)]
    return cropped_img

#extract the numbers out of the string output of ocr
def extract_numbers(string):
    similar = False
    for line in string.splitlines():
        val = ""
        for ch in line:
            if ch.isdigit():
                val = val + ch
        if len(val) == 13:
            if int(val) <= int(end[1]) and int(val) >int(start[1]):
                for t in timestamps:
                    if t[1] == val:
                        timestamps.append([filename, 'r'])
                        similar = True
                if similar == False:
                    timestamps.append([filename, val])
                return val
    timestamps.append([filename, 'r'])
    return 'r'

#rename the frame to its corresponding timestamp
def rename(filepath, timestamps):

    for filename in os.listdir(filepath):
        if filename.endswith('.jpg'):
            for i in timestamps:
                if i[0] == filename:
                    newfilename = filepath + "\\" + i[1]
                    if not os.path.isfile(newfilename+'.jpg') :
                        print(filepath + "\\" + filename + "--------" + filepath + "\\" + str(i[1]) + '.jpg')
                        os.rename(filepath + "\\" + filename, newfilename + '.jpg')

                    else:
                        print(filepath + "\\" + filename + "--------" + filepath + "\\" + newfilename + '_' +filename )
                        os.rename(filepath + "\\" + filename, newfilename + '_' +filename )

#to rename frames that were unable to be detected a name by the ocr
def linear_interpolation(t_stamps):
    print(t_stamps)

    last_tstamp = t_stamps[0]
    ctr = -1
    renamed_tstamps = []
    t = t_stamps[1]
    i = 1
    while t:
        if last_tstamp:
            ctr = ctr + 1
        i=i+1
        if not t[1] == 'r' and renamed_tstamps:
            next_tstamp = t
            eq_val = (int(next_tstamp[1]) - int(last_tstamp[1]))/(ctr+1)

            n = 1
            for v in renamed_tstamps:
                v[1] = str(int(int(last_tstamp[1]) + (eq_val*n)))
                n=n+1
            last_tstamp = []
            ctr = 0
            renamed_tstamps.clear()
        elif t[1] == 'r':
            if not last_tstamp:
                last_tstamp = t_stamps[i-2]
            renamed_tstamps.append(t)
        if i < len(t_stamps):
            t = t_stamps[i]
        else:
            t = []
    print("---------------------------------")
    for i in t_stamps:
        i[0] = str(i[0]) + '.jpg'
    return t_stamps

timestamps = []
for filename in os.listdir(filepath):
    if filename.endswith('.jpg'):


        print(str(filename))
        file = filepath + '\\'+filename
        msg = file

        #img = cv2.imread(file)

        client = vision.ImageAnnotatorClient()

        with io.open(file, 'rb') as image_file:
            content = image_file.read()

        #read characters in image and place into string
        #content = cv2.imencode('.jpg', img)[1].tostring()
        image = vision.types.Image(content=content)


        response = client.text_detection(image=image)

        #strg =pytesseract.image_to_string(img, config='--psm 6')
        if response.text_annotations:
            full_text = str(response.text_annotations[0])
            strg = full_text.split("bounding_poly")[0]
            strg = strg.split("description: ")[1]
            strg = strg.replace("\\n", "\n")
        else:
            strg = ""
        extract_numbers(strg)

t_stamps = []

#remove extension on names
for i in timestamps:
    t_val = int(i[0].replace('.jpg', ''))
    t_stamps.append([t_val, i[1]])

t_stamps.sort()
t_stamps[0] = start
t_stamps[len(t_stamps)-1] = end

#rename the missing timestamps using linear interpolation
line1 = copy.deepcopy(t_stamps)
renamed_timestamps = linear_interpolation(t_stamps)
print(renamed_timestamps)
rename(filepath, renamed_timestamps)
write_to_file(filepath, line1, renamed_timestamps)


