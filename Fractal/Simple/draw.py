import sys
import colorsys
import json
from PIL import Image
from PIL import ImageDraw

dimensions = (300, 200)
scaling_factor = 4
n_iterations = 150
colors_max = 50

poly = [complex(0.3, 0.3), 1, 0, 0, 1]
threshold = 2

r_start = 0.78
r_coef = - 0.55
g_start = 0.9
g_coef = - 0.6
b_start = 0
b_coef = 0.8
speed = 15
dark2light = True



def create_palette(r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light = True):

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


def draw():
    palette = create_palette(r_start, r_coef, g_start, g_coef, b_start, b_coef, speed, dark2light)

    center = (scaling_factor / 2, (scaling_factor / 2) * dimensions[1]/dimensions[0])

    img = Image.new("RGB", dimensions)
    d = ImageDraw.Draw(img)

    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            z = complex(x * scaling_factor / dimensions[0] - center[0], y * scaling_factor / dimensions[0] - center[1])
            n = iterate(z, poly, threshold, n_iterations)

            if n is None:
                v = 1
            else:
                v = n/float(n_iterations)

            d.point((x, y), fill = palette[int(v * (colors_max - 1))])

    del d

    img.save("result.png")

draw()
    
