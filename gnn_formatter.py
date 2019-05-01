#!/usr/bin/env python2

##
#
# Reads data from a specified directory, reformats it, and saves
# it in a format that is readable by a GNN.
#
# Input:
#    - a directory from the SDD that contains an annotations.txt file and a
#      corresponding video.mov file.
#    - a unique name for this example 
#
# Output
#    - A attribute file with the following format:
#         =======================================
#         | time   node_id   attributes         |
#         |                                     |
#         |                                     |
#
#       where the attributes include
#           - position (of center of bounding box)
#           - width (of bounding box)
#           - height (of bounding box)
#           - node_type (pedestrian, bike, etc)
#           - inside (average pixel value inside the box)
#           - above (average pixel value just above the box)
#           - below (average pixel value just below the box)
#           - left (average pixel value just left of the box)
#           - right (average pixel value just right of the box)
#
##

import sys
import csv
import cv2
import numpy as np

# ==================== Helper Functions =======================

def label_int(label_string):
    """
    Maps a label ('Pedestrian', 'Biker', 'Car') to an integer (1,2,3).
    """
    if label_string == 'Pedestrian':
        return 1
    elif label_string == 'Biker':
        return 2
    elif label_string == 'Car':
        return 3
    else:
        raise NameError("Unknown label type %s" % label_string)

def box_center(xmin, ymin, xmax, ymax):
    """
    Return the center of the bounding box
    """
    x_mean = np.mean([xmin, xmax])
    y_mean = np.mean([ymin, ymax])

    return (x_mean, y_mean)

def box_width_height(xmin, ymin, xmax, ymax):
    """
    Return the width and height of the bounding box
    """
    width = xmax-xmin
    height = ymax-ymin

    return (width, height)

def pixel_avgs(cap, frame, xmin, ymin, xmax, ymax):
    """
    Return the average pixel values within, above, below, left, and right
    of the bounding box. 
    """
    have_img, img = cap.read()  # this automatically iterates to the next frame

    margin = 20   # how many pixels in each direction to consider

    within_img = img[ymin:ymax, xmin:xmax]
    above_img = img[ymin-margin:ymin, xmin:xmax]
    below_img = img[ymax:ymax+margin, xmin:xmax]
    right_img = img[ymin:ymax, xmax:xmax+margin]
    left_img = img[ymin:ymax, xmin-margin:xmin]

    ## Overlay a red rectangle on the bounding box for debugging
    #highlight_img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0,0,255),3)
    #cv2.imshow('image',highlight_img)
    #cv2.waitKey(1)

    within_avg = average_color(within_img)
    above_avg = average_color(above_img)
    below_avg = average_color(below_img)
    right_avg = average_color(right_img)
    left_avg = average_color(left_img)

    return (within_avg, above_avg, below_avg, right_avg, left_avg)

def average_color(img):
    """
    Return the average [B,G,R] color values in the given cv2 image
    """
    avg_color_per_row = np.mean(img, axis=0)
    avg_color = np.mean(avg_color_per_row, axis=0)

    return avg_color

# ==================== Main Parsing Script =======================

def main(input_dir, output_dir, name):

    annotations_file = input_dir + "/annotations.txt"
    video_file = input_dir + "/video.mov"
    data_file = output_dir + "/" + name + ".attributes"

    # load the annotations file with csv
    input_file = open(annotations_file,'r')
    reader = csv.reader(input_file, delimiter=" ")

    # load the output file for writing
    output_file = open(data_file,'w')
    writer = csv.writer(output_file, delimiter=" ")

    # load the video with cv2
    cap = cv2.VideoCapture(video_file)

    # Write a header
    header = ["#", "frame", "node_id", "position_x", "position_y", "width", "height", "type", 
                                   "center_blue", "center_green", "center_red",
                                   "above_blue", "above_green", "above_red",
                                   "below_blue", "below_green", "below_red",
                                   "right_blue", "right_green", "right_red",
                                   "left_blue", "left_green", "left_red"]

    writer.writerow(header)

    last_node_id = 0
    for line in reader:
        row_data = []   # this is what we'll (eventually) write to the file

        # unpack some attributes
        node_id = int(line[0])  # unique identifier of the node
        xmin = int(line[1]) # Bounding Box Coordinates: (0,0) ---- +x 
        ymin = int(line[2]) #                             |
        xmax = int(line[3]) #                             |  
        ymax = int(line[4]) #                            +y
        frame = int(line[5]) # frame # 
        label = line[9]      # Pedestrian, Biker, Car

        # Determine whether we've changed to considering a new node: if so, we need to reset the
        # video reader
        if node_id != last_node_id:
            cap.set(1,frame)
            last_node_id = node_id

        # Derive the values we'll actually put in the file
        x_position, y_position = box_center(xmin, ymin, xmax, ymax)
        width, height = box_width_height(xmin, ymin, xmax, ymax)

        # Map the label to an integer
        node_type = label_int(label)

        # get average pixel values around the node
        within_avg, above_avg, below_avg, right_avg, left_avg = pixel_avgs(cap, frame, xmin, ymin, xmax, ymax)

        # Add data to write
        row_data.append(frame)
        row_data.append(node_id)
        row_data.append(x_position)
        row_data.append(y_position)
        row_data.append(width)
        row_data.append(height)
        row_data.append(node_type)

        row_data += list(within_avg)    # each pixel average is a list of [blue green red] values, 
        row_data += list(above_avg)    # so we can append in this way
        row_data += list(below_avg)
        row_data += list(left_avg)
        row_data += list(right_avg)
        
        writer.writerow(row_data)

    input_file.close()
    output_file.close()

if __name__=="__main__":
    if len(sys.argv) != 4:
        print("Usage: %s [input_directory] [output_directory] [output_filename]" % sys.argv[0])
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    name = sys.argv[3]

    main(input_dir, output_dir, name)

