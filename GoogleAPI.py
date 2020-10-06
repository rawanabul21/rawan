from __future__ import print_function
from google.cloud import vision
import os
import io
import cv2


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Rawan\\OneDrive\\Documents\\University\\Thesis\\key.json"

path = 'C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\91.png'

img = cv2.imread(path)
content = cv2.imencode('.jpg', img)[1].tostring()
image = vision.types.Image(content=content)

client = vision.ImageAnnotatorClient()
response = client.text_detection(image=image)

#for text in response.text_annotations[0]:
    #print('=' * 30)
    #print(text.description)
    #vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
    #print('bounds:', ",".join(vertices))
if response:
    full_text = str(response.text_annotations[0])
    words = full_text.split("bounding_poly")[0]
    words = words.split("description: ")[1]
    words = words.replace("\\n", "\n")
    print(words)