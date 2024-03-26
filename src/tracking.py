import cv2

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

class MyTracker:

    """
    My own tracker based on CSRT algorithm

    args:
        mode:
            1 -> tracking from a video
            2 -> tracking from multiple images
        src:
            the source video or the first image

    """

    def __init__(self, mode, src):
        
        self.mode = mode;
        
        """
        if self.mode == 1:
            try:
                self.sourcePath = cv2.VideoCapture(src)
            except:
                print("Error: Cannot open the source path.")
                print("Error: Capture from camera as an alternative.")
                self.sourcePath = cv2.VideoCapture(0)
        else:
            print("Error: Please specify the mode:")
            print("Error: 1 -> tracking from a video")
            print("Error: 2 -> tracking from multiple images")
            return
        """
        self.sourcePath = cv2.VideoCapture(src)
        ok, self.frame = self.sourcePath.read()

        # select bounding box

        print("MyTracker: Please select the bounding box")
        self.bbox = cv2.selectROI(self.frame, False)
        print(f"MyTracker: bbox: {self.bbox}")
        
        # set tracker
        print("MyTracker: Setting tracker...")
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(self.frame, self.bbox)
        print("MyTracker: Setting tracker... done")

    def updateFrame(self, frame):
        # update current frame with given image
        self.frame = frame

    def getFrame(self):

        if self.mode == 1:
            ok, self.frame = self.sourcePath.read()
            if not ok:
                print("Error: Cannot open the source path")
                return (ok, self.frame)
        elif self.mode == 2:
            pass

        return (1, self.frame)

    def updateTracking(self):
        # call this function in your main loop
        self.timer = cv2.getTickCount()
        ok, self.frame = self.getFrame()
        if not ok:
            return -1

        ok, self.bbox = self.tracker.update(self.frame)
        self.fps = cv2.getTickFrequency() / (cv2.getTickCount() - self.timer)

        if ok:
            cv2.rectangle(self.frame, (self.bbox[0], self.bbox[1]), 
                        (self.bbox[0]+self.bbox[2], self.bbox[1]+self.bbox[3]), (255,0,0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(self.frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(self.frame, "CSRT Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0),2);
     
        # Display FPS on frame
        cv2.putText(self.frame, "FPS : " + str(int(self.fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2);
 
        # Display result
        cv2.imshow("Tracking", self.frame)
        
        return (1, (self.bbox[0] + self.bbox[2]/2, self.bbox[1] + self.bbox[3]/2))


