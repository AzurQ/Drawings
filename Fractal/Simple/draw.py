import sys
import os
import json
import itertools
import argparse
from functions import to_list, list_of_list_transform, extract_poly, create_palette, generate_result_path, draw_image, write_inputs

# Draw a fractal from given inputs
## Inputs may be provided as lists - all possibilites are produced
def draw(folder_save, display = False, draw_input_file = "draw-inputs.json", image_number = 0):
    # folder_save (str) is path to folder where results should be saved
    # display (bool) indicates if plots should be prompted
    # draw_input_file (str) is path to input file
    # image_number (int) is the starting number for the images to be saved (in their names)

    # Load input file
    with open(draw_input_file) as json_file:
        inputs = json.load(json_file)[0]

    # Convert color options into lists to iterate on
    input_to_convert_list_1 = ["r_start", "r_coef", "g_start", "g_coef", "b_start", "b_coef", "speed", "dark2light", "colors_max"]
    for item in input_to_convert_list_1:
        inputs[item] = to_list(inputs[item])

    # Iterate for color options in input file
    for r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max in itertools.product(inputs["r_start"], inputs["r_coef"], inputs["g_start"], inputs["g_coef"], inputs["b_start"], inputs["b_coef"], inputs["speed"], inputs["dark2light"], inputs["colors_max"]):

        # Create the graphical palette
        palette = create_palette(r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max)

        # Dict used for saving/writing specific input data
        input_dict = {"r_start": r_start, "r_coef": r_coef, "g_start": g_start, "g_coef": g_coef, "b_start": b_start, "b_coef": b_coef, "speed": speed, "dark2light": dark2light, "colors_max": colors_max}

        # Some color options may be incompatible - they are not considered
        if palette is not None:

            # Convert graphical options into lists to iterate on
            inputs["dimensions"]["x"] = to_list(inputs["dimensions"]["x"])
            inputs["dimensions"]["y"] = to_list(inputs["dimensions"]["y"])
            input_to_convert_list_2 = ["n_iterations", "threshold", "scaling_factor", "right_shift", "upward_shift"]
            for item in input_to_convert_list_2:
                inputs[item] = to_list(inputs[item])

            # Iterate for graphical options in input file
            for n_iterations, threshold, scaling_factor, right_shift, upward_shift, dimension_x, dimension_y in itertools.product(inputs["n_iterations"], inputs["threshold"], inputs["scaling_factor"], inputs["right_shift"], inputs["upward_shift"], inputs["dimensions"]["x"], inputs["dimensions"]["y"]):

                # Update dict used for saving/writing specific input data
                input_dict["n_iterations"] = n_iterations
                input_dict["threshold"] = threshold
                input_dict["scaling_factor"] = scaling_factor
                input_dict["right_shift"] = right_shift
                input_dict["upward_shift"] = upward_shift
                input_dict["dimensions"] = {"x": dimension_x, "y": dimension_y}
                dimensions = [dimension_x, dimension_y]

                # Import the dictionnary of polynomial
                poly_raw_list = extract_poly(inputs["polynomial"])
                # Make the list of polynomials implicitely defined in the dictionnary
                poly_list = list_of_list_transform(poly_raw_list)

                # Iterate for each polynomial
                for poly in poly_list:

                    # Generate save paths
                    path, input_path = generate_result_path(folder_save)
                    # Plot and save image
                    draw_image(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, palette, colors_max, display)
                    # Save image input data
                    write_inputs(input_path, poly, input_dict, image_number)
                    # Update image number (int) for saving
                    image_number += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default=None, type = str,
                        help="Folder path for result saving (str)")
    parser.add_argument("-d", "--display", default=False, type = bool,
                        help="Display plots (bool)")
    parser.add_argument("-i", "--input", default="draw-inputs.json", type = str,
                        help="Drawing input path (str)")
    parser.add_argument("-n", "--number", default=0,
                        help="Start image number (int)")
    args = parser.parse_args()

    draw(args.folder, args.display, args.input, int(args.number))
