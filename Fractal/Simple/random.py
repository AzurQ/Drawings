import sys
import os
import json
import numpy
from functions import draw

# Draw a fractal from given inputs and random inputs
## Randomly generated inputs from the latter file override inputs from the former
## Inputs may be provided as lists - all possibilites are produced
def random(folder_save, display = False):




if __name__ == "__main__":
    # Without any iput, executable saves images in Result folder without ploting them
    if len(sys.argv) == 1:
        random(None)
    else
        folder_save = sys.argv[1]:
        # If save folder is specified, images and inputs are saved within
        if len(sys.argv) == 2:
            random(folder_save)
        else:
            display = sys.argv[2]
            random(folder_save, display)
