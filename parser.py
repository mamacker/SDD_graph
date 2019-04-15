#!/usr/bin/env python3

##
#
# A quick script to construct a graph from pedestrian
# tracking data from the Stanford Drone Dataset
#
##

import numpy as np
import sys
import csv

class Pedestrian:
    """
    A simple object that represents a pedestrian. It has
    two attributes: x and y position.
    """
    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position

    def distance(self, other_node):
        """
        Return the distance between this and another
        pedestrian object.
        """
        return np.sqrt((self.x-other_node.x)**2+(self.y-other_node.y)**2)

class PedestrianGraph:
    """
    The graph we will use for prediction. Each node is a Pedestrian,
    and nodes are connected if they are closer than a threshold. 
    """
    def __init__(self, threshold=3):
        # The nodes are each Pedestrian objects
        self.nodes = []   

        # Edges are represented as a list of tuples of Pedestrian objects
        self.edges = []

        # Nodes are connected if and only if they are within this
        # distance threshold of each other
        self.thresh = threshold

    def add_node(self, node):
        """
        Add a node to the graph
        """
        # Include this node
        self.nodes.append(node)

        # Construct edges where necessary
        pass

    def plot(self):
        """
        Use matplotlib to make a pretty plot of the graph
        """
        pass

def parse(filename):
    """
    Return PedestrianGraph objects correponding to the data in the
    specified annotation file.

    Annotation file format:
    Each line in the annotations.txt file corresponds to an annotation. Each line contains 10+ columns, 
    separated by spaces. The definition of these columns are:

	1   Track ID. All rows with the same ID belong to the same path.
	2   xmin. The top left x-coordinate of the bounding box.
	3   ymin. The top left y-coordinate of the bounding box.
	4   xmax. The bottom right x-coordinate of the bounding box.
	5   ymax. The bottom right y-coordinate of the bounding box.
	6   frame. The frame that this annotation represents.
	7   lost. If 1, the annotation is outside of the view screen.
	8   occluded. If 1, the annotation is occluded.
	9   generated. If 1, the annotation was automatically interpolated.
	10  label. The label for this annotation, enclosed in quotation marks.

    """
    with open(filename,'r') as inpt:
        reader = csv.reader(inpt, delimiter=" ")
        for line in reader:
            print(line)


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: %s [annotation file]" % sys.argv[0])
        sys.exit(1)

    fname = sys.argv[1]   # file with raw data

    parse(fname)
