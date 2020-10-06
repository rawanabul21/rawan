# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import  os

video = 'C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\videos\\test11a.MOV'
path = 'C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\output_screenshots\\test11a_framesfaster'


fvs = FileVideoStream(video).start()
time.sleep(1.0)
# start the FPS timer
fps = FPS().start()
i=1
# loop over frames from the video file stream
while fvs.more():
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale (while still retaining 3
	# channels)
    frame = fvs.read()
    frame = imutils.resize(frame, width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])
    cv2.imwrite(os.path.join(path, str(i) + '.jpg'), frame)
    i +=1
    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()