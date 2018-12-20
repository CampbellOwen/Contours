from PIL import Image
import cv2
import tifffile as tiff
import numpy as np
from quadtree import QuadTree
import turtle
from isoline import get_lines
from isoline import equal_path
import svgwrite
import itertools


orig = tiff.imread('data/sfu-centered.tif')
height, width = orig.shape

small = orig

print("Creating quad tree...", end='', flush=True)
img = QuadTree(small, 0, 0, small.shape[1]-1, small.shape[0]-1)
print(" Done")
img_max = small.max()
img_min = small.min()
thresholds = [1+img_min+(t*img_max) for t in np.linspace(0, 1, 20)]
print(thresholds)
print("Creating isolines...", end='', flush=True)
path_sets = [get_lines(img, thresh) for thresh in thresholds]
print(" Done")
min_x = 0
min_y = 0

max_x = 0
max_y = 0

for path_set in path_sets:
    for path in path_set:
        for pt in path:
            if pt[0] < min_x:
                min_x = pt[0]
            elif pt[1] > max_x:
                max_x = pt[0]
            if pt[1] < min_y:
                min_y = pt[1]
            elif pt[1] > max_y:
                max_y = pt[1]

# colours = ["#59bec1", '#e47558', '#2488a7', '#69c198']
# colours = [
#     "#4357AD",
#     "#DF928E",
#     '#9D6A89',
#     '#8A89C0',
#     '#48A9A6'
# ]
# colours = ["#ffffff"]
# colours = [
#     '#114b5f',
#     '#7b0828',
#     '#628395',
#     '#cca43b'
# ]
colours = [
    '#2c514c',
    '#af8d86',
    '#434371',
    '#8693ab'
]
# background = "#161021"
# background = "#000000"
background = "#0F0E0E"
dwg = svgwrite.Drawing("out/sfu-centered-3.svg", (max_x-min_x, max_y-min_y))
dwg.add(dwg.rect(insert=(0,0), size=(max_x-min_x, max_y-min_y)).stroke("none").fill(background))
for i, path_set in enumerate(path_sets):
    for line in path_set:
        curr_colour = colours[ i % len(colours) ]
        path_data = [f"M{line[0][0]} {line[0][1]}"]
        for pt in line[1:-1]:
            path_data.append(f"L{pt[0]} {pt[1]}")
        if equal_path(line[-1], line[0]):
            path_data.append("Z")
        else:
            path_data.append(f"L{line[-1][0]} {line[-1][1]}")
        dwg.add(dwg.path(d="".join(path_data)).stroke(curr_colour).fill("none"))
    print(f"Finished Elevation level {i+1}")
dwg.save()

# lines = get_lines(img, 31.9)

# for t in np.linspace(0,1, 10):
#     threshold = 1 + (t * (small.max()-10))
# # threshold = 31.9

#     lines = get_lines(img, threshold)

#     for line in lines:
#         path = ["M {} {} ".format(line[0][0], line[0][1])]
#         for p in line[1:]:
#             path.append("L {} {}".format(p[0], p[1]))
#         dwg.add(dwg.path(d="".join(path)).stroke(color="#000000").fill("none"))
# dwg.save()
# t = turtle.Turtle()
# turtle.setup(small.shape[1], small.shape[0], startx=0, starty=0)

# for line in lines:
#     for i,pos in enumerate(line):
#         if i == 0:
#             t.up()
#             t.setpos(pos[0], pos[1])
#             t.down()
#         else:
#             t.goto(pos[0], pos[1])
# input()



    # curr = small.copy()
    # curr[curr < threshold] = 0
    # curr[curr >= threshold] = 1
    # tree = QuadTree(curr, 0, 0, curr.shape[1], curr.shape[0])
    # Image.fromarray(np.uint8(curr*255)).save(f'out/thresholds/alt/{threshold}.png')
