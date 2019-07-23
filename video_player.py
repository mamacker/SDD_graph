#!/usr/bin/env python2

##
#
# Script for playing a video file to find the interesting examples
#
##

import sys
import cv2
import numpy as np

#video_file = sys.argv[1];
video_file = "./SDD/nexus/video0/video.mov"

cap = cv2.VideoCapture(video_file)

have_img = True
frame = 1
paused = False
while have_img:
    if paused:
        print("Paused at frame %s" % frame)

        print("Press [space] to resume or [b] to go back 10s")
        next_key = cv2.waitKey(0)

        if next_key == 32:
            # Resume playing the video
            paused = False
        elif next_key == 98:
            # Go back 100 frames
            frame = frame - 100
            print("resetting to frame %s" %frame)
            cap.set(1,frame)
        else:
            # Stay paused
            print("Invalid key %s" % next_key)

        print(next_key)
    else:

        # interate to next frame
        have_img, img = cv2.VideoCapture.read(cap)

        cv2.imshow('image',img)
        key = cv2.waitKey(10)

        print(frame)

        if key == 32:
            paused = True
        
        frame += 1

    

cv2.destroyAllWindows()

