import sys
import os
import json
import numpy
from functions import draw

# Draw a fractal from given inputs and random distribution for given inputs
## Fixed inputs may be provided as lists - all possibilites are produced
## Randomly generated inputs override general fixed inputs
def random(draw_input_dict, random_intput_dict, folder_save, display = False, image_number = 0):
    # draw_input_dict (doct) is dictionnary with fixed parameters
    # random_intput_dict (dict) is dictionnary with random parameter distributions
    # folder_save (str) is path to folder where results should be saved
    # display (bool) indicates if plots should be prompted
    # image_number (int) is the starting number for the images to be saved (in their names)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default=None, type = str,
                        help="Folder path for result saving (str)")
    parser.add_argument("-d", "--display", default=False, type = bool,
                        help="Display plots (bool)")
    parser.add_argument("-i", "--input", default="Inputs/draw-inputs.json", type = str,
                        help="Drawing input path (str)")
    parser.add_argument("-r", "--random", default="Inputs/random-inputs.json", type = str,
                        help="Random input path (str)")
    parser.add_argument("-n", "--number", default=0,
                        help="Start image number (int)")
    args = parser.parse_args()

    # Load fixed input file
    with open(args.input) as draw_json_file:
        draw_input_dict = json.load(draw_json_file)[0]

    # Load random input file
    with open(args.random) as random_json_file:
        random_intput_dict = json.load(random_json_file)[0]

    random(draw_input_dict, random_intput_dict, args.folder, args.display, int(args.number))
