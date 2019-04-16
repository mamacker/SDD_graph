#!/usr/bin/env python3

##
#
# A quick script to construct a graph from pedestrian
# tracking data from the Stanford Drone Dataset
#
##

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

class Pedestrian:
    """
    A simple object that represents a pedestrian. It has
    two attributes: x and y position.
    """
    def __init__(self, x_position, y_position, label):
        self.x = x_position
        self.y = y_position

        self.type = label   # pedestrian, biker, etc

    def distance(self, other_node):
        """
        Return the distance between this and another
        pedestrian object.
        """
        return np.sqrt((self.x-other_node.x)**2+(self.y-other_node.y)**2)

    def __str__(self):
        return "Node at (%s,%s)" % (self.x, self.y)

class PedestrianGraph:
    """
    The graph we will use for prediction. Each node is a Pedestrian,
    and nodes are connected if they are closer than a threshold.
    """
    def __init__(self, threshold=400):
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
        # Construct edges where necessary
        for other_node in self.nodes:
            if node.distance(other_node) < self.thresh:
                self.edges.append((node,other_node))
        
        # Include this node in the graph
        self.nodes.append(node)

    def plot(self, ax):
        """
        Use matplotlib to make a pretty plot of the graph
        """
        for node in self.nodes:
            if node.type == "Pedestrian":
                color='red'
            elif node.type == "Biker":
                color='blue'
            else:
                color='green'

            ax.scatter(node.x,node.y,color=color,marker='o')

        for edge in self.edges:
            ax.plot([edge[0].x,edge[1].x],[edge[0].y,edge[1].y],linestyle='--',color='grey')


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
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    xlim = (200,1800)
    ylim = (200,1800)

    for frame in range(509):
        graph = PedestrianGraph()
        with open(filename,'r') as inpt:
            reader = csv.reader(inpt, delimiter=" ")

            for line in reader:
                if int(line[5]) == frame and not int(line[6]):   # select elements in the given frame and within the field of view
                    # Position of the object = center of bounding box
                    x = np.mean([int(line[1]),int(line[3])])
                    y = np.mean([int(line[2]),int(line[3])])
                    label = line[9]

                    node = Pedestrian(x,y,label)
                    graph.add_node(node)

        ax.clear()   # Get rid of previously plotted elements
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        graph.plot(ax)
        plt.pause(0.005)

    plt.show()



if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: %s [annotation file]" % sys.argv[0])
        sys.exit(1)

    fname = sys.argv[1]   # file with raw data

    parse(fname)
