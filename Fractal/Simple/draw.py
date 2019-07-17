import sys
import os
import json
import itertools
from functions import to_list, list_of_list_transform, extract_poly, create_palette, generate_result_path, draw, write_inputs

def draw(folder_save, display = False):
    image_number = 0

    with open('draw-inputs.json') as json_file:
        inputs = json.load(json_file)[0]


    input_to_convert_list_1 = ["r_start", "r_coef", "g_start", "g_coef", "b_start", "b_coef", "speed", "dark2light", "colors_max"]
    for item in input_to_convert_list_1:
        inputs[item] = to_list(inputs[item])


    for r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max in itertools.product(inputs["r_start"], inputs["r_coef"], inputs["g_start"], inputs["g_coef"], inputs["b_start"], inputs["b_coef"], inputs["speed"], inputs["dark2light"], inputs["colors_max"]):

        palette = create_palette(r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max)
        input_dict = {"r_start": r_start, "r_coef": r_coef, "g_start": g_start, "g_coef": g_coef, "b_start": b_start, "b_coef": b_coef, "speed": speed, "dark2light": dark2light, "colors_max": colors_max}
        if palette is not None:

            inputs["dimensions"]["x"] = to_list(inputs["dimensions"]["x"])
            inputs["dimensions"]["y"] = to_list(inputs["dimensions"]["y"])
            input_to_convert_list_2 = ["n_iterations", "threshold", "scaling_factor", "right_shift", "upward_shift"]
            for item in input_to_convert_list_2:
                inputs[item] = to_list(inputs[item])

            for n_iterations, threshold, scaling_factor, right_shift, upward_shift, dimension_x, dimension_y in itertools.product(inputs["n_iterations"], inputs["threshold"], inputs["scaling_factor"], inputs["right_shift"], inputs["upward_shift"], inputs["dimensions"]["x"], inputs["dimensions"]["y"]):

                input_dict["n_iterations"] = n_iterations
                input_dict["threshold"] = threshold
                input_dict["scaling_factor"] = scaling_factor
                input_dict["right_shift"] = right_shift
                input_dict["upward_shift"] = upward_shift
                input_dict["dimensions"] = {"x": dimension_x, "y": dimension_y}
                dimensions = [dimension_x, dimension_y]

                poly_raw_list = extract_poly(inputs["polynomial"])
                poly_list = list_of_list_transform(poly_raw_list)
                for poly in poly_list:

                    path, input_path = generate_result_path(folder_save)
                    draw(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, palette, colors_max, display)
                    write_inputs(input_path, poly, input_dict, image_number)
                    image_number += 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        draw(None)
    else:
        folder_save = sys.argv[1]
        if len(sys.argv) == 2:
            draw(folder_save)
        else:
            display = sys.argv[2]
            print(display)
            draw(folder_save, display)
