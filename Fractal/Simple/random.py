import sys
import os
import json
import numpy
from functions import draw

# Draw a fractal from given inputs and random distribution for given inputs
## Fixed inputs may be provided as lists - all possibilites are produced
## Randomly generated inputs override general fixed inputs
def random(folder_save, display = False, draw_input_file = "draw-inputs.json", random_input_file = "random-inputs.json", image_number = 0):
    # folder_save (str) is path to folder where results should be saved
    # display (bool) indicates if plots should be prompted
    # draw_input_file (str) is path to input file containing fixed parameters
    # random_input_file (str) is path to input file containing random parameter distributions
    # image_number (int) is the starting number for the images to be saved (in their names)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default=None, type = str,
                        help="Folder path for result saving (str)")
    parser.add_argument("-d", "--display", default=False, type = bool,
                        help="Display plots (bool)")
    parser.add_argument("-i", "--input", default="draw-inputs.json", type = str,
                        help="Drawing input path (str)")
    parser.add_argument("-r", "--random", default="random-inputs.json", type = str,
                        help="Random input path (str)")
    parser.add_argument("-n", "--number", default=0,
                        help="Start image number (int)")
    args = parser.parse_args()

    random(args.folder, args.display, args.input, args.random, int(args.number))
