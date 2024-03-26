from tracking import MyTracker
import cv2

videoPath = "../media/car.mkv"
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



