from tracking import MyTracker
import cv2
import numpy as np
import time
from datetime import datetime

YELLOW = (255, 0, 255)
BLUE   = (255,0,0)
BLACK  = (0,0,0)
OLIVE  = (0,128,128)

videoPath = "../media/hello2.mp4"
tracker = MyTracker(1, videoPath)

historyPosition = []

while True:

    status, pos = tracker.updateTracking()
    
    if status == -1:
        break

    historyPosition.append(pos)
    
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break


cv2.destroyAllWindows()

# save the position in text file
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_time.replace(":", "-")
with open(f"track_{current_time}.txt", "w") as f:
    for i in range(len(historyPosition)):
        f.write("%d %d\n" % (historyPosition[i][0], historyPosition[i][1]))

print("showing the path")
firstImg = tracker.firstFrame
width   = firstImg.shape[0]
height  = firstImg.shape[1]

i = 0
while True:
    cv2.imshow("Path", firstImg) 

    currentPos = historyPosition[i]
    cv2.circle(firstImg, (int(currentPos[0]), int(currentPos[1])), 5, OLIVE, cv2.FILLED)
    if i < len(historyPosition)-1:
        i += 1
    time.sleep(0.007)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

