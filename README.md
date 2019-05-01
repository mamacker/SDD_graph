# SDD Graph Utilities

Some utilities for extracting graph data from the [Stanford Drone Dateset](http://cvgl.stanford.edu/projects/uav_data/)

## Dependencies

- python3
- numpy
- matplotlib
- csv

## Usage

The script `parser.py` extracts data from a annotation file
of the SDD and plays an animation of an associated graph over time:

e.g.
`./parser.py ./SDD/quad/video0/annotations.txt`

gives rise to a visualization like this:
![example graph](sdd_graph_example.gif)

where bikes are shown in blue, pedestrians are red, and nodes are connected if they are
closer than a given threshold. 


The script `gnn_formatter.py` extracts data from an annotation file and a video
from a given directory of the SDD and creates a space-delimited annotations file with the following columns:

    - time/frame number
    - node id number
    - x position of the center of the bounding box
    - y position of the center of the bounding box
    - width of the bounding box
    - height of the bounding box
    - node type (1 for Pedestrian, 2 for Bicycle, 3 for Car)

    - average Blue color within the bounding box
    - average Green color within the bounding box
    - average Red color within the bounding box

    - average Blue color above the bounding box
    - average Green color above the bounding box
    - average Red color above the bounding box

    - average Blue color below the bounding box
    - average Green color below the bounding box
    - average Red color below the bounding box

    - average Blue color left of the bounding box
    - average Green color left of the bounding box
    - average Red color left of the bounding box

    - average Blue color right of the bounding box
    - average Green color right of the bounding box
    - average Red color right of the bounding box

For example, `./gnn_formatter.py ./SDD/quad/video0/ ./data quad_video0` reads from `./SDD/quad/video0/annotations.txt` 
and `./SDD/quad/video0/video.mov` to generate the file `./data/quad_video0.attributes`.


