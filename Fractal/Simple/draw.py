import sys
import os
import json
import itertools
import argparse
from progress.bar import Bar
from functions import to_list, extract_poly, create_palette, generate_result_path, draw_image, write_inputs, create_poly_list, count_plots

# Draw a fractal from given inputs
## Inputs may be provided as lists - all possibilites are produced
def draw(draw_input_dict, folder_save, display = False, image_number = 0, cartesian_poly = True):
    # draw_input_dict (dict) is dictionary with all inputs
    # folder_save (str) is path to folder where results should be saved
    # display (bool) indicates if plots should be prompted
    # image_number (int) is the starting number for the images to be saved (in their names)
    # cartesian_poly (bool) indicates if polynomials are considered by taking the cartesian product of all coefficient values
        ## It is only used for the random_draw.py script which allows to called an unique list of polynomials that would not be converted to its cartesian product

    # Define progress bar
    progress = Bar('Processing', max = count_plots(draw_input_dict, cartesian_poly))

    # Convert color options into lists to iterate on
    input_to_convert_list_1 = ["r_start", "r_coef", "g_start", "g_coef", "b_start", "b_coef", "speed", "dark2light", "colors_max"]
    for item in input_to_convert_list_1:
        draw_input_dict[item] = to_list(draw_input_dict[item])

    # Iterate for color options in input file
    for r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max in itertools.product(draw_input_dict["r_start"], draw_input_dict["r_coef"], draw_input_dict["g_start"], draw_input_dict["g_coef"], draw_input_dict["b_start"], draw_input_dict["b_coef"], draw_input_dict["speed"], draw_input_dict["dark2light"], draw_input_dict["colors_max"]):

        # Create the graphical palette
        palette = create_palette(r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max)

        # Dict used for saving/writing specific input data
        output_dict = {"r_start": r_start, "r_coef": r_coef, "g_start": g_start, "g_coef": g_coef, "b_start": b_start, "b_coef": b_coef, "speed": speed, "dark2light": dark2light, "colors_max": colors_max}

        # Some color options may be incompatible - they are not considered
        if palette is not None:

            # Convert graphical options into lists to iterate on
            draw_input_dict["dimensions"]["x"] = to_list(draw_input_dict["dimensions"]["x"])
            draw_input_dict["dimensions"]["y"] = to_list(draw_input_dict["dimensions"]["y"])
            input_to_convert_list_2 = ["n_iterations", "threshold", "scaling_factor", "right_shift", "upward_shift"]
            for item in input_to_convert_list_2:
                draw_input_dict[item] = to_list(draw_input_dict[item])

            # Iterate for graphical options in input file
            for n_iterations, threshold, scaling_factor, right_shift, upward_shift, dimension_x, dimension_y in itertools.product(draw_input_dict["n_iterations"], draw_input_dict["threshold"], draw_input_dict["scaling_factor"], draw_input_dict["right_shift"], draw_input_dict["upward_shift"], draw_input_dict["dimensions"]["x"], draw_input_dict["dimensions"]["y"]):

                # Update dict used for saving/writing specific input data
                output_dict["n_iterations"] = n_iterations
                output_dict["threshold"] = threshold
                output_dict["scaling_factor"] = scaling_factor
                output_dict["right_shift"] = right_shift
                output_dict["upward_shift"] = upward_shift
                output_dict["dimensions"] = {"x": dimension_x, "y": dimension_y}
                dimensions = [dimension_x, dimension_y]

                # Create the list of polynomials to iterate
                poly_list = create_poly_list(draw_input_dict["polynomial"], cartesian_poly)

                # Iterate for each polynomial
                for poly in poly_list:

                    # Generate save paths
                    path, input_path = generate_result_path(folder_save)
                    # Plot and save image
                    draw_image(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, palette, colors_max, display)
                    # Save image input data
                    write_inputs(input_path, poly, output_dict, image_number)
                    # Update image number (int) for saving
                    image_number += 1
                    # Update progress bar
                    progress.next()

    progress.finish()


if __name__ == "__main__":
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default=None, type = str,
                        help="Folder path for result saving (str)")
    parser.add_argument("-d", "--display", default=False, type = bool,
                        help="Display plots (bool)")
    parser.add_argument("-i", "--input", default="Inputs/draw-inputs.json", type = str,
                        help="Drawing input path (str)")
    parser.add_argument("-n", "--number", default=0,
                        help="Start image number (int)")
    args = parser.parse_args()

    # Load input file
    with open(args.input) as json_file:
        draw_input_dict = json.load(json_file)

    draw(draw_input_dict, args.folder, args.display, int(args.number))
