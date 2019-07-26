import sys
import os
import json
import colorsys
from PIL import Image
from PIL import ImageDraw
import itertools
import numpy
from math import cos, sin, pi, sqrt

# List of graphical color parameters
color_params = ["x_start", "x_coef", "y_start", "y_coef", "z_start", "z_coef", "speed", "dark2light", "colors_max", "color_system"]


# Put an object into a list if not already a list
def to_list(x):
    if not isinstance(x, list):
        x = [x]
    return(x)


# Compute the list of all polynomials defined by cartesian product from a polynomial degree coefficient list
def cartesian_product(list):
    new_list = []
    for degree in range(len(list)):
        # Initialize list with list of all degree 0 coefficients
        if len(new_list) == 0:
            new_list = [[x] for x in list[degree]]
        else:
            temp_list = []
            # Current list append a new coefficient for each coefficient in all combinaisons found for the next coefficient, such that all possibilities are created
            for value in list[degree]:
                temp_list = temp_list + [x + [value] for x in new_list]
            new_list = temp_list
    return(new_list)


# Extract a dictionary containing polynomial coefficient to a list whose indexes account for degree
def extract_poly(dict):
    poly_list = []
    for key in dict:
        # If some degree coefficients are not specified, 0 are added instead
        if len(poly_list) <= int(key):
            poly_list = poly_list + [to_list(0) for _ in range(int(key) - len(poly_list) + 1)]
        # Depending on specified real/imaginary parts for a given coefficient, all combinaisons are appended to the next coefficient
        if "imaginary" in dict[key]:
            if "real" in dict[key]:
                poly_list[int(key)] = [complex(a, b) for (a, b) in itertools.product(to_list(dict[key]["real"]), to_list(dict[key]["imaginary"]))]
            else:
                poly_list[int(key)] = [complex(0, b) for b in to_list(dict[key]["imaginary"])]
        else:
            poly_list[int(key)] = [a for a in to_list(dict[key]["real"])]
    return(poly_list)


# Return the maximum length of a coefficient list inside a polynomial dictionary (real/imaginary parts nested in degree dictionaries)
def find_poly_dict_max_length(poly_dict):
    n = 0
    for degree in poly_dict:
        for part in poly_dict[degree]:
            if len(to_list(poly_dict[degree][part])) > n :
                n = len(to_list(poly_dict[degree][part]))
    return(n)


# Merge two lists defining real and imaginary parts into a list of complex numbers
def list_to_complex(real_list, imaginary_list):
    # If one of the list if of length 1, it is distributed for all values of the another list
    if len(real_list) == 1:
        return([complex(real_list[0], x) for x in imaginary_list])
    elif len(imaginary_list) == 1:
        return([complex(x, imaginary_list[0]) for x in real_list])
    # Else, the values are distributed one by one to form complex numbers if the lengths of the two list match
    elif len(real_list) == len(imaginary_list):
        return([complex(real_list[i], imaginary_list[i]) for i in range(len(real_list))])
    else:
        raise Exception("Lists must be of equal size or one of them should be of length 1.")


# Converting a polynomial dictionary into a dictionary containing complex coefficient lists
def poly_dict_to_complex_dict(poly_dict):
    complex_dict = {}
    # Value of dictionary for each degree is replaced with a new list of complex numbers
    for degree in poly_dict:
        # If real or imaginary parts are not specified, they are put to 0 in order to call list_to_complex function
        if "real" not in poly_dict[degree]:
            poly_dict[degree]["real"] = [0]
        if "imaginary" not in poly_dict[degree]:
            poly_dict[degree]["imaginary"] = [0]
        # Real and imaginary parts are merged into complex list
        complex_dict[degree] = list_to_complex(to_list(poly_dict[degree]["real"]), to_list(poly_dict[degree]["imaginary"]))
    return(complex_dict)


# Create the polynomial list from polynomial dictionary
def create_poly_list(poly_dict, cartesian_poly):
    # Normal pathway of drawing script
    if cartesian_poly:
        # Import the dictionary of polynomial
        poly_raw_list = extract_poly(poly_dict)
        # Make the list of polynomials implicitely defined in the dictionary
        poly_list = cartesian_product(poly_raw_list)
    # If polynomials are generated without cartesian product by only taking term-to-term combinaisons
    else:
        # Prepare output list with size determined by global_poly_number that may be found back in the input dictionary
        global_poly_number = find_poly_dict_max_length(poly_dict)
        poly_list = [[] for _ in range(global_poly_number)]

        # Convert input dictionary into complex dictionary
        complex_dict = poly_dict_to_complex_dict(poly_dict)

        # Make the list of polynomial explicitely defined in the dictionary
        for degree in complex_dict:
            # If some degree coefficients are not specified, 0 are added instead
            if len(poly_list[0]) <= int(degree):
                poly_list = [x + [0 for _ in range(int(degree) - len(poly_list[0]))] for x in poly_list]
            # Distribute polynomial coefficient list to existing list
            poly_list = distribute_list(poly_list, complex_dict[degree], global_poly_number)
    return(poly_list)


# Extract color palette parameter subdictionary from an input dictionary
def extract_color_palette_dict(dict):
    color_palette_dict = {}
    for parameter in dict:
        if parameter in color_params:
            color_palette_dict[parameter] = dict[parameter]
    return(color_palette_dict)


# Return the maximum length of a coefficient list of a color palette subdictionary
def find_color_palette_dict_max_length(color_palette_dict):
    n = 0
    for parameter in color_palette_dict:
        if len(to_list(color_palette_dict[parameter])) > n:
            n = len(to_list(color_palette_dict[parameter]))
    return(n)


# Distribute a new list at the end of all elements of a list of lists
def distribute_list(list_of_lists, new_list, theorical_list_length):
    # If only one parameter is specified for a coefficient, it is distributed for all lists
    if len(new_list) == 1:
        list_of_lists = [x + to_list(new_list[0]) for x in list_of_lists]
        return(list_of_lists)
    # For randomly generated parameters, each value is distributed to a different list rather than making cartesian product
    elif len(new_list) == theorical_list_length:
        list_of_lists = [list_of_lists[i] + to_list(new_list[i]) for i in range(theorical_list_length)]
        return(list_of_lists)
    else:
        raise Exception("For non-cartesian product parameters generation (polynomial and/or color palette), all parameters in fixed input file should be single values and not lists.")


# Create the color palette list from input subdictionary
def create_color_palette_list(draw_input_dict, cartesian_color_palette = True):
    # Normal pathway of drawing script
    if cartesian_color_palette:
        return(itertools.product(draw_input_dict["x_start"], draw_input_dict["x_coef"], draw_input_dict["y_start"], draw_input_dict["y_coef"], draw_input_dict["z_start"], draw_input_dict["z_coef"], draw_input_dict["speed"], draw_input_dict["dark2light"], draw_input_dict["colors_max"], draw_input_dict["color_system"]))
    # If color palettes are generated without cartesian product by only taking term-to-term combinaisons
    else:
        # Prepare output list with size determined by global_color_palette_number that may be found back in the input dictionary
        color_palette_dict = extract_color_palette_dict(draw_input_dict)
        global_color_palette_number = find_color_palette_dict_max_length(color_palette_dict)
        color_palette_list = [[] for _ in range(global_color_palette_number)]

        # Make the color palette list explicitely defined in the dictionary
        for color_param in color_params:
            color_palette_list = distribute_list(color_palette_list, color_palette_dict[color_param], global_color_palette_number)

    return(color_palette_list)


# Create a color palette from color progression functions
def create_palette(x_start, x_coef, y_start, y_coef, z_start, z_coef, speed, dark2light, colors_max, color_system):
    # Remove unfeasible combinations of color palette (i.e. RGB values out of [0:255])
    if (x_start < 0) or (x_start > 1):
        # print("\nx_start is ill-defined")
        return(None)
    if (y_start < 0) or (y_start > 1):
        # print("\ny_start is ill-defined")
        return(None)
    if (z_start < 0) or (z_start > 1):
        # print("\nz_start is ill-defined")
        return(None)
    if (x_start + x_coef < 0) or (x_start + x_coef > 1):
        # print("\nx_coef is ill-defined")
        return(None)
    if (y_start + y_coef < 0) or (y_start + y_coef > 1):
        # print("\ny_coef is ill-defined")
        return(None)
    if (z_start + z_coef < 0) or (z_start + z_coef > 1):
        # print("\nz_coef is ill-defined")
        return(None)

    # Initialize color palette
    palette = [0] * colors_max

    for i in range(colors_max):
        # Define progression of color palette from one side to another (i.e. how fast colors are evolving)
        if dark2light:
            f = 1 - abs((float(i) / colors_max - 1) ** speed)
        else:
            f = abs((float(i) / colors_max - 1) ** speed)

        # Define color palette coefficients from functions for each RGB coefficient
        ## If RGB, x codes for red, y for green, and z for blue
        if color_system == "rgb" or color_system == "RGB":
            r, g, b = x_start + f * x_coef, y_start + f * y_coef, z_start + f * z_coef
        # If HSV system, x codes for hue, y for saturation, and z for value
        elif color_system == "hsv" or color_system == "HSV":
            r, g, b = colorsys.hsv_to_rgb(x_start + f * x_coef, y_start + f * y_coef, z_start + f * z_coef)
        else:
            raise Exception("Color system is not defined. Only RGB and HSV are available.")
        palette[i] = (int(r*255), int(g*255), int(b*255))
    return(palette)


# Iterate a polynomial from a starting point and return first divergence time from a threshold
def iterate(z, poly, threshold, n_iterations):
    p = len(poly)
    for n in range(n_iterations + 1):
        z = sum(poly[i] * (z ** i) for i in range(p))
        if abs(z) > threshold:
            return n
    return None


# Iterate two polynomials and combine results
def iterate_combo(z, poly1, poly2, combo_method, threshold, n_iterations):
    n1 = iterate(z, poly1, threshold, n_iterations)
    n2 = iterate(z, poly2, threshold, n_iterations)
    if n1 is None or n2 is None:
        return None
    else:
        if combo_method == "sum":
            return((n1 + n2) / 2)
        elif combo_method == "mult":
            return(sqrt(n1 * n2))
        elif combo_method == "max":
            return(max(n1, n2))
        elif combo_method == "min":
            return(min(n1, n2))
        elif combo_method == "diff":
            return(abs(n1 - n2))


# Generate save path from folder name
def generate_result_path(folder_save):
    path = "Results/"
    input_path = "Results/Inputs/"
    if folder_save is not None:
        # Define save paths
        input_path = path + str(folder_save) + "/Inputs/"
        path = path + str(folder_save) + "/"
    # Create paths if they not already exist
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    return(path, input_path)


# Indicates if an image already exists
def exist(image_number, path):
    return(os.path.exists(path + str(image_number) + ".png"))


# Draw a fractal image from inputs and save image
def draw_image(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, rotation, palette, colors_max, display = False, combo = False, poly2 = None, combo_method = None):

    # Define center of the image
    center = (scaling_factor / 2, (scaling_factor / 2) * dimensions[1]/dimensions[0])

    # Initialize image
    img = Image.new("RGB", dimensions)
    d = ImageDraw.Draw(img)

    # Iterate on two-dimensional canvas
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            # Define starting point
            z = complex(x * scaling_factor / dimensions[0] - center[0] - right_shift, y * scaling_factor / dimensions[0] - center[1] + upward_shift) * complex(cos(rotation * pi / 180), sin(rotation * pi / 180))

            # Return convergence value
            if not combo:
                n = iterate(z, poly, threshold, n_iterations)
            else:
                n = iterate_combo(z, poly, poly2, combo_method, threshold, n_iterations)

            # Transform convergence value into color intensity
            if n is None:
                v = 1
            else:
                v = n/float(n_iterations)

            # Add point to the image
            d.point((x, y), fill = palette[int(v * (colors_max - 1))])

    # Save image and plot if asked
    img.save(path + str(image_number) + ".png")
    if display:
        img.show()
    del d


# Add a polynomial to a dictionnary
def add_poly_to_dict(poly, dict, key_name):
    dict[key_name] = {}
    for degree in range(len(poly)):
        if poly[degree] != 0:
            # Write non-nul coefficients
            dict[key_name][str(degree)] = {}
            if poly[degree].real != 0:
                (dict[key_name][str(degree)])["real"] = (poly[degree]).real
            if poly[degree].imag != 0:
                (dict[key_name][str(degree)])["imaginary"] = (poly[degree]).imag
    return(dict)


# Save inputs of a given image
def write_inputs(input_path, poly, input_dict, image_number, poly2 = None):
    # Copy input file data
    output_file = input_dict.copy()
    # Generate the polynomial dictionary of current data
    if poly2 is None:
        output_file = add_poly_to_dict(poly, output_file, "polynomial")
    # Save two polynomials if fractal combo
    else:
        output_file = add_poly_to_dict(poly, output_file, "polynomial1")
        output_file = add_poly_to_dict(poly2, output_file, "polynomial2")

    # Save input file data
    with open(input_path + str(image_number) + "-draw-inputs.json", 'w') as f:
        json.dump(output_file, f)


# Generate random samples from a given distribution
## If global_sample_number is not None, generate samples with given sample number
def generate_from_distribution(distribution_dict, global_sample_number = None):
    # Remove ill-defined dictionaries
    if len(distribution_dict) != 1:
        print("Distribution dictionary is not well defined")
        return(None)
    # Supported distribution are normal, binomial, and uniform distributions
    for key in distribution_dict:
        if key == "normal":
            mean = distribution_dict[key]["mean"]
            std = distribution_dict[key]["std"]
            samples = distribution_dict[key]["samples"] if global_sample_number is None else global_sample_number
            return(list(numpy.random.normal(mean, std, samples)))
        elif key == "binomial":
            n = distribution_dict[key]["n"]
            p = distribution_dict[key]["p"]
            samples = distribution_dict[key]["samples"] if global_sample_number is None else global_sample_number
            return([float(x) for x in list(numpy.random.binomial(n, p, samples))])
        elif key == "extended_binomial":
            n = distribution_dict[key]["n"]
            p = distribution_dict[key]["p"]
            samples = distribution_dict[key]["samples"] if global_sample_number is None else global_sample_number
            return(extended_binomial(n, p, samples))
        elif key == "uniform":
            low_bound = distribution_dict[key]["low_bound"]
            high_bound = distribution_dict[key]["high_bound"]
            samples = distribution_dict[key]["samples"] if global_sample_number is None else global_sample_number
            return(list(numpy.random.uniform(low_bound, high_bound, samples)))
        else:
            print("Distribution not recognized")
            return(None)


# Binomial distribution function centered on 0 between -n and n
def extended_binomial(n, p, samples):
    return([float(x) - n for x in list(numpy.random.binomial(2 * n, p, samples))])


# Generate a sub-drawing_input_dict from a random_input_dict by replacing distributions with their random samples
def generate_random_inputs(random_input_dict, global_poly_number = None, global_color_palette_number = None):
    randomly_generated_dict = {}
    # Parse on different dictionary parmeters, and parse within them if nested dictionaries
    for parameter in random_input_dict:
        if parameter == "polynomial" or parameter == "polynomial1" or parameter == "polynomial2":
            if parameter not in randomly_generated_dict:
                randomly_generated_dict[parameter] = {}
            # Polynomial are splitted into degree dictionaries
            for degree in random_input_dict[parameter]:
                if degree not in randomly_generated_dict[parameter]:
                    randomly_generated_dict[parameter][degree] = {}
                # Polynomial coefficients are splitted into real and imaginary part dictionaries
                for part in random_input_dict[parameter][degree]:
                    # If distribution is not recognized or ill-defined, override is cancelled
                    if generate_from_distribution(random_input_dict[parameter][degree][part], global_poly_number) is not None:
                        randomly_generated_dict[parameter][degree][part] = generate_from_distribution(random_input_dict[parameter][degree][part], global_poly_number)
        elif parameter == "dimensions":
            if parameter not in randomly_generated_dict:
                randomly_generated_dict[parameter] = {}
            # Dimension canvas is splitted into x and y axis dictionaries
            for dimension in random_input_dict[parameter]:
                if generate_from_distribution(random_input_dict[parameter][dimension], global_poly_number) is not None:
                    randomly_generated_dict[parameter][dimension] = generate_from_distribution(random_input_dict[parameter][dimension], global_poly_number)
        elif parameter in color_params:
            if generate_from_distribution(random_input_dict[parameter], global_color_palette_number) is not None:
                randomly_generated_dict[parameter] = generate_from_distribution(random_input_dict[parameter], global_color_palette_number)
        else:
            if generate_from_distribution(random_input_dict[parameter], global_poly_number) is not None:
                randomly_generated_dict[parameter] = generate_from_distribution(random_input_dict[parameter], global_poly_number)
    return(randomly_generated_dict)


# Override a drawing_input dictionaries with inputs generated from a random dictionary inside a sub-dictionary
def override(draw_input_dict, random_input_dict):
    # Parse on different dictionary parmeters, and parse within them if nested dictionaries
    for parameter in random_input_dict:
        if parameter == "polynomial" or parameter == "polynomial1" or parameter == "polynomial2":
            for degree in random_input_dict[parameter]:
                if degree not in draw_input_dict[parameter]:
                    draw_input_dict[parameter][degree] = {}
                for part in random_input_dict[parameter][degree]:
                    draw_input_dict[parameter][degree][part] = random_input_dict[parameter][degree][part]
        elif parameter == "dimensions":
            for dimension in random_input_dict[parameter]:
                draw_input_dict[parameter][dimension] = random_input_dict[parameter][dimension]
        else:
            draw_input_dict[parameter] = random_input_dict[parameter]
    return(draw_input_dict)


# Compute the total number of drawings to plot
def count_plots(input_dict, cartesian_poly = True, cartesian_color_palette = True):
    n = 1
    # Flag to only count once color palette parameters when used in non-cartesian random generation
    color_palette_ok_flag = False
    # Compute the size of the cartesian product of all parameters
    for parameter in input_dict:
        if parameter == "dimensions":
            for dimension in input_dict["dimensions"]:
                n *= len(to_list(input_dict["dimensions"][dimension]))
        elif parameter == "polynomial" or parameter == "polynomial1" or parameter == "polynomial2":
            if cartesian_poly:
                for degree in input_dict[parameter]:
                    for part in input_dict[parameter][degree]:
                        n *= len(to_list(input_dict[parameter][degree][part]))
            # If polynomials are randomly generated without cartesian product, the global_poly_number is used
            else:
                n *= find_poly_dict_max_length(input_dict[parameter])
        elif (parameter in color_params) and not cartesian_color_palette:
            if not color_palette_ok_flag:
                n *= find_color_palette_dict_max_length(extract_color_palette_dict(input_dict))
                color_palette_ok_flag = True
        else:
            n *= len(to_list(input_dict[parameter]))
    return(n)
