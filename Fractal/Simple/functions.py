import sys
import os
import colorsys
import json
from PIL import Image
from PIL import ImageDraw
import itertools

# Put an object into a list if not already a list
def to_list(x):
    if not isinstance(x, list):
        x = [x]
    return(x)

# Compute the list of all polynomials defined by cartesian product from a polynomial degree coefficient list
def list_of_list_transform(list):
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

# Extract a dictionnary containing polynomial coefficient to a list whose indexes account for degree
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

# Create a color palette from color progression functions
def create_palette(r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max):
    # Remove unfeasible combinations of color palette (i.e. RGB values out of [0:255])
    if (r_start < 0) or (r_start > 1):
        print("r_start is ill-defined")
        return(None)
    if (g_start < 0) or (g_start > 1):
        print("g_start is ill-defined")
        return(None)
    if (b_start < 0) or (b_start > 1):
        print("b_start is ill-defined")
        return(None)
    if (r_start + r_coef < 0) or (r_start + r_coef > 1):
        print("r_coef is ill-defined")
        return(None)
    if (g_start + g_coef < 0) or (g_start + g_coef > 1):
        print("g_coef is ill-defined")
        return(None)
    if (b_start + b_coef < 0) or (b_start + b_coef > 1):
        print("b_coef is ill-defined")
        return(None)

    # Initialize color palette
    palette = [0] * colors_max

    for i in range(colors_max):
        # Define progression of color palette from one side to another (i.e. how fast colors are evolving)
        if dark2light:
            f = 1 + (float(i) / colors_max - 1) ** speed
        else:
            f = - (float(i) / colors_max - 1) ** speed

        # Define color palette coefficients from functions for each RGB coefficient
        r, g, b = colorsys.hsv_to_rgb(r_start + f * r_coef, g_start + f * g_coef, b_start + f * b_coef)
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

# Draw a fractal image from inputs and save image
def draw_image(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, palette, colors_max, display = False):

    # Define center of the image
    center = (scaling_factor / 2, (scaling_factor / 2) * dimensions[1]/dimensions[0])

    # Initialize image
    img = Image.new("RGB", dimensions)
    d = ImageDraw.Draw(img)

    # Iterate on two-dimensional canvas
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            # Define starting point
            z = complex(x * scaling_factor / dimensions[0] - center[0] - right_shift, y * scaling_factor / dimensions[0] - center[1] + upward_shift)
            # Return convergence value
            n = iterate(z, poly, threshold, n_iterations)

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

# Save inputs of a given image
def write_inputs(input_path, poly, input_dict, image_number):
    # Copy input file data
    output_file = input_dict.copy()
    # Generate the polynomial dictionnary of current data
    for degree in range(len(poly)):
        if poly[degree] != 0:
            # Write non-nul coefficients
            output_file[str(degree)] = {}
            if poly[degree].real != 0:
                (output_file[str(degree)])["real"] = (poly[degree]).real
            if poly[degree].imag != 0:
                (output_file[str(degree)])["imaginary"] = (poly[degree]).imag
    # Save input file data
    with open(input_path + str(image_number) + "-draw-inputs.json", 'w') as f:
        json.dump(output_file, f)
