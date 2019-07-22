import sys
import os
import json
import argparse
from draw import draw
from functions import generate_random_inputs, override

# Draw a fractal from given inputs and random distribution for given inputs
## Fixed inputs may be provided as lists - all possibilites are produced
## Randomly generated inputs override general fixed inputs
def random_draw(draw_input_dict, random_input_dict, folder_save, display = False, image_number = 0, global_poly_number = None):
    # draw_input_dict (doct) is dictionary with fixed parameters
    # random_input_dict (dict) is dictionary with random parameter distributions
    # folder_save (str) is path to folder where results should be saved
    # display (bool) indicates if plots should be prompted
    # image_number (int) is the starting number for the images to be saved (in their names)
    # global_poly_number (int) is - if not None - the number of polynomials to generate and to used in plots to be constructed thanks to all coefficient distributions without regard to cartesian product

    # random_input_dict is used to generate input list to override fixed inputs
    ## If global_poly_number is not None, polynomial list is constructed explicitely
    new_input_dict = override(draw_input_dict, generate_random_inputs(random_input_dict, global_poly_number))

    # draw function is called with generated inputs
    draw(new_input_dict, folder_save, display = False, image_number = 0, cartesian_poly = (global_poly_number is None))


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
    parser.add_argument("-p", "--polynomial", default=None, type = int,
                        help="If filled, number of different polynomial to generate with all coefficient distribution, without passing to cartesian product (int)")
    args = parser.parse_args()

    # Load fixed input file
    with open(args.input) as draw_json_file:
        draw_input_dict = json.load(draw_json_file)

    # Load random input file
    with open(args.random) as random_json_file:
        random_input_dict = json.load(random_json_file)

    random_draw(draw_input_dict, random_input_dict, args.folder, args.display, int(args.number), args.polynomial)
