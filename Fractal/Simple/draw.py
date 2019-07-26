import sys
import os
import json
import itertools
import argparse
from progress.bar import Bar

# Import Common.functions
sys.path.insert(1, "/Users/azur/git/Drawings/Fractal/Common")
from functions import to_list, extract_poly, create_palette, generate_result_path, draw_image, write_inputs, create_poly_list, create_color_palette_list, count_plots, exist, color_params

# Draw a fractal from given inputs
## Inputs may be provided as lists - all possibilites are produced
def draw(draw_input_dict, folder_save, display = False, continued = False, image_number = 0, cartesian_poly = True, cartesian_color_palette = True):
    # draw_input_dict (dict) is dictionary with all inputs
    # folder_save (str) is path to folder where results should be saved
    # display (bool) indicates if plots should be prompted
    # continued (bool) indicates if draw should be restarted or if should continued from already existing plots
    # image_number (int) is the starting number for the images to be saved (in their names)
    # cartesian_poly (bool) indicates if polynomials are considered by taking the cartesian product of all coefficient values
        ## It is only used for the random_draw.py script which allows to call an unique list of polynomials that would not be converted to its cartesian product
    # cartesian_color_palette (bool) indicates if color palette parameters are considered by taking the cartesian product of all coefficient values
        ## It is only used for the random_draw.py script which allows to call an unique list of color palettes that would not be converted to its cartesian product

    # Define progress bar
    progress = Bar('Processing', max = count_plots(draw_input_dict, cartesian_poly, cartesian_color_palette))

    # Generate save paths
    path, input_path = generate_result_path(folder_save)

    # Convert color options into lists to iterate on
    for item in color_params:
        draw_input_dict[item] = to_list(draw_input_dict[item])

    # Iterate for color options in input file
    for x_start, x_coef, y_start, y_coef, z_start, z_coef, speed, dark2light, colors_max, color_system in create_color_palette_list(draw_input_dict, cartesian_color_palette):

        # Create the graphical palette
        palette = create_palette(x_start, x_coef, y_start, y_coef, z_start, z_coef, speed, dark2light, colors_max, color_system)

        # Dict used for saving/writing specific input data
        output_dict = {"x_start": x_start, "x_coef": x_coef, "y_start": y_start, "y_coef": y_coef, "z_start": z_start, "z_coef": z_coef, "speed": speed, "dark2light": dark2light, "colors_max": colors_max, "color_system": color_system}

        # Some color options may be incompatible - they are not considered
        if palette is None:
            # Update progress bar anyway to keep track
            progress.next()
        else:
            # Convert graphical options into lists to iterate on
            draw_input_dict["dimensions"]["x"] = to_list(draw_input_dict["dimensions"]["x"])
            draw_input_dict["dimensions"]["y"] = to_list(draw_input_dict["dimensions"]["y"])
            input_to_convert_list_2 = ["n_iterations", "threshold", "scaling_factor", "right_shift", "upward_shift", "rotation"]
            for item in input_to_convert_list_2:
                draw_input_dict[item] = to_list(draw_input_dict[item])

            # Iterate for graphical options in input file
            for n_iterations, threshold, scaling_factor, right_shift, upward_shift, rotation, dimension_x, dimension_y in itertools.product(draw_input_dict["n_iterations"], draw_input_dict["threshold"], draw_input_dict["scaling_factor"], draw_input_dict["right_shift"], draw_input_dict["upward_shift"], draw_input_dict["rotation"], draw_input_dict["dimensions"]["x"], draw_input_dict["dimensions"]["y"]):

                # Update dict used for saving/writing specific input data
                output_dict["n_iterations"] = n_iterations
                output_dict["threshold"] = threshold
                output_dict["scaling_factor"] = scaling_factor
                output_dict["right_shift"] = right_shift
                output_dict["upward_shift"] = upward_shift
                output_dict["rotation"] = rotation
                output_dict["dimensions"] = {"x": dimension_x, "y": dimension_y}
                dimensions = [dimension_x, dimension_y]

                # Create the list of polynomials to iterate
                poly_list = create_poly_list(draw_input_dict["polynomial"], cartesian_poly)

                # Iterate for each polynomial
                for poly in poly_list:

                    # If continued, image should not already exist
                    if not continued or not exist(image_number, path):
                        # Plot and save image
                        draw_image(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, rotation, palette, colors_max, display)
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
    parser.add_argument("-c", "--continued", default=False, type = bool,
                        help="If image number already exists, pass (bool)")
    args = parser.parse_args()

    # Load input file
    with open(args.input) as json_file:
        draw_input_dict = json.load(json_file)

    draw(draw_input_dict, args.folder, args.display, args.continued, int(args.number))
