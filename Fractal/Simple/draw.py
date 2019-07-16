import sys
import os
import colorsys
import json
from PIL import Image
from PIL import ImageDraw
import itertools

def main(folder_save):
    image_number = 0


    def to_list(x):
        if not isinstance(x, list):
            x = [x]
        return(x)


    def list_of_list_transform(list):
        new_list = []
        for degree in range(len(list)):
            if len(new_list) == 0:
                new_list = [[x] for x in list[degree]]
            else:
                temp_list = []
                for value in list[degree]:
                    temp_list = temp_list + [x + [value] for x in new_list]
                new_list = temp_list
        return(new_list)


    def extract_poly(dict):
        poly_list = []
        for key in dict:
            if len(poly_list) <= int(key):
                poly_list = poly_list + [to_list(0) for _ in range(int(key) - len(poly_list) + 1)]
            if "imaginary" in dict[key]:
                if "real" in dict[key]:
                    poly_list[int(key)] = [complex(a, b) for (a, b) in itertools.product(to_list(dict[key]["real"]), to_list(dict[key]["imaginary"]))]
                else:
                    poly_list[int(key)] = [complex(0, b) for b in to_list(dict[key]["imaginary"])]
            else:
                poly_list[int(key)] = [a for a in to_list(dict[key]["real"])]
        return(poly_list)


    def create_palette(r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light, colors_max):
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

        palette = [0] * colors_max

        for i in range(colors_max):
            if dark2light:
                f = 1 + (float(i) / colors_max - 1) ** speed
            else:
                f = - (float(i) / colors_max - 1) ** speed
            r, g, b = colorsys.hsv_to_rgb(r_start + f * r_coef, g_start + f * g_coef, b_start + f * b_coef)

            palette[i] = (int(r*255), int(g*255), int(b*255))

        return(palette)


    def iterate(z, poly, threshold, n_iterations):
        p = len(poly)
        for n in range(n_iterations + 1):
            z = sum(poly[i] * (z ** i) for i in range(p))
            if abs(z) > threshold:
                return n
        return None


    def generate_result_path(folder_save):
        path = "Results/"
        input_path = path
        if folder_save is not None:
            path = path + str(folder_save) + "/"
            input_path = input_path + str(folder_save) + "/"
            if not os.path.exists(input_path):
                os.makedirs(input_path)
        return(path, input_path)


    def draw(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, palette):

        center = (scaling_factor / 2, (scaling_factor / 2) * dimensions[1]/dimensions[0])

        img = Image.new("RGB", dimensions)
        d = ImageDraw.Draw(img)

        for x in range(dimensions[0]):
            for y in range(dimensions[1]):
                z = complex(x * scaling_factor / dimensions[0] - center[0] - right_shift, y * scaling_factor / dimensions[0] - center[1] + upward_shift)
                n = iterate(z, poly, threshold, n_iterations)

                if n is None:
                    v = 1
                else:
                    v = n/float(n_iterations)

                d.point((x, y), fill = palette[int(v * (colors_max - 1))])

        img.save(path + str(image_number) + ".png")
        del d


    def write_inputs(input_path, poly, input_dict):
        output_file = input_dict.copy()
        for degree in range(len(poly)):
            if poly[degree] != 0:
                output_file[str(degree)] = {}
                if poly[degree].real != 0:
                    (output_file[str(degree)])["real"] = (poly[degree]).real
                if poly[degree].imag != 0:
                    (output_file[str(degree)])["imaginary"] = (poly[degree]).imag
        with open(input_path + str(image_number) + "-inputs.json", 'w') as f:
            json.dump(output_file, f)


    with open('inputs.json') as json_file:
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
                    draw(path, image_number, poly, n_iterations, dimensions, threshold, scaling_factor, right_shift, upward_shift, palette)
                    write_inputs(input_path, poly, input_dict)
                    image_number += 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(None)
    else:
        folder_save = sys.argv[1]
        main(folder_save)
