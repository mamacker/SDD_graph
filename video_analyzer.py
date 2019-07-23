#!/usr/bin/env python2

##
#
# Script for extracting colors from video file
#
##

import cv2
import numpy as np

def average_color(img):
    """
    Returns the average [B G R] values in a given cv2 image
    """
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    return avg_color

video_file = "./SDD/quad/video0/video.mov"

cap = cv2.VideoCapture(video_file)

have_img = True
while have_img:
    # interate to next frame
    have_img, img = cv2.VideoCapture.read(cap)

    if have_img:
        # crop to given range
        xmin = 573
        ymin = 508
        xmax = 704
        ymax = 635


        crop_img = img[ymin:ymax,xmin:xmax]

        cv2.imshow('image',crop_img)
        cv2.waitKey(100)

        print(average_color(crop_img))

cv2.destroyAllWindows()

