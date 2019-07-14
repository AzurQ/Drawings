import sys
import os
import colorsys
import json
from PIL import Image
from PIL import ImageDraw

def main(folder_save):

    with open('inputs.json') as json_file:
        inputs = json.load(json_file)[0]

    dimensions = (inputs["dimensions"]["x"], inputs["dimensions"]["y"])
    scaling_factor = inputs["scaling_factor"]
    n_iterations = inputs["n_iterations"]
    colors_max = inputs["colors_max"]

    threshold = inputs["threshold"]

    r_start = inputs["r_start"]
    r_coef = inputs["r_coef"]
    g_start = inputs["g_start"]
    g_coef = inputs["g_coef"]
    b_start = inputs["b_start"]
    b_coef = inputs["b_coef"]
    speed = inputs["speed"]
    dark2light = inputs["dark2light"]

    upward_shift = inputs["upward_shift"]
    right_shift = inputs["right_shift"]


    def extract_poly(dict):
        poly = []
        for key in dict:
            if len(poly) <= int(key):
                poly = poly + [0 for _ in range(int(key) - len(poly) + 1)]
            if "imaginary" in dict[key]:
                if "real" in dict[key]:
                    poly[int(key)] = complex(dict[key]["real"], dict[key]["imaginary"])
                else:
                    poly[int(key)] = complex(0, dict[key]["imaginary"])
            else:
                poly[int(key)] = dict[key]["real"]
        return(poly)


    def create_palette():
        if (r_start < 0) or (r_start > 1):
            raise ValueError("r_start is ill-defined")
        if (g_start < 0) or (g_start > 1):
            raise ValueError("g_start is ill-defined")
        if (b_start < 0) or (b_start > 1):
            raise ValueError("b_start is ill-defined")
        if (r_start + r_coef < 0) or (r_start + r_coef > 1):
            raise ValueError("r_coef is ill-defined")
        if (g_start + g_coef < 0) or (g_start + g_coef > 1):
            raise ValueError("g_coef is ill-defined")
        if (b_start + b_coef < 0) or (b_start + b_coef > 1):
            raise ValueError("b_coef is ill-defined")

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


    def draw(folder_save):
        palette = create_palette()
        poly = extract_poly(inputs["polynomial"])

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

        path = "Results/"
        if folder_save is not None:
            path = path + str(folder_save) + "/"
            if not os.path.exists(path):
                os.makedirs(path)
        img.save(path + "1.png")
        with open(path + "1-inputs.json", 'w') as f:
            json.dump(inputs, f)

        del d

    draw(folder_save)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(None)
    else:
        folder_save = sys.argv[1]
        main(folder_save)
