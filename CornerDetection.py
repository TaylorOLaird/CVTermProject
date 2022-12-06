# -*- coding: utf-8 -*-
"""Computer Vision Term Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U81LWJUDa6hIcRcyfkcQEXf1aPp-vct2
"""

from PIL import Image
import requests
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
from skimage.color import rgb2gray

"""# Harris Corner Detection"""

basePath = 'TestImages/'
fileName = ['IMG_0530.JPEG', 'IMG_0531.JPEG', 'IMG_0532.JPEG',
            'IMG_0533.JPEG', 'IMG_0534.JPEG', 'IMG_0535.JPEG', ]
img = Image.open(basePath + fileName[0])
img_array = np.array(img)
gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
gray_image

# corner detection with openCv
# from google.colab.patches import cv2_imshow

img = cv2.imread(basePath + fileName[5])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.04)
colorCorners = 255, 0, 0  # 0, 0, 255

# BGR point changes
# anywhere the corner (local max of the grandient matrix) is present change the pixel to red
img[dst > 0.01 * dst.max()] = [colorCorners]
# cv2.imshow(img)
fig, axs = plt.subplots(1, 1)
axs.imshow(img)
fig.set_figheight(10)
fig.set_figwidth(10)

locationX, locationY = np.where((img == (colorCorners)).all(axis=2))

coordinates = [(locationX[i], locationY[i]) for i in range(len(locationX))]

def euclideanDistance(point1, center):
    return math.sqrt(sum((point1 - center) ** 2))


def findMaxCorner(points, center):
    Distances = []
    for coordinate in points:
        Distances.append(euclideanDistance(np.array(coordinate), center))
    position = np.argmax(Distances)

    return points[position]


# get the lowest top-left coordinates
# the cross of these are the center
# values below each are top left, above x and above y are top right
# values above each are bottom right, below x above y are bottom left

xDivision = (max(locationX) - min(locationX)) // 2 + min(locationX)
yDivision = (max(locationY) - min(locationY)) // 2 + min(locationY)
topLeft, topRight, bottomLeft, bottomRight = [], [], [], []
center = [xDivision, yDivision]

for coordinate in coordinates:
    if coordinate[0] < xDivision and coordinate[1] < yDivision:
        topLeft.append(coordinate)
    elif coordinate[0] < xDivision and coordinate[1] > yDivision:
        topRight.append(coordinate)
    elif coordinate[0] > xDivision and coordinate[1] < yDivision:
        bottomLeft.append(coordinate)
    elif coordinate[0] > xDivision and coordinate[1] > yDivision:
        bottomRight.append(coordinate)

topLeft = findMaxCorner(topLeft, center)
topRight = findMaxCorner(topRight, center)
bottomLeft = findMaxCorner(bottomLeft, center)
bottomRight = findMaxCorner(bottomRight, center)

# original code for finding the average of a cluster of points

# topLeft = tuple(np.floor(np.array(topLeft).mean(0)))
# topRight = tuple(np.floor(np.array(topRight).mean(0)))
# bottomLeft = tuple(np.floor(np.array(bottomLeft).mean(0)))
# bottomRight = tuple(np.floor(np.array(bottomRight).mean(0)))

print(
    f"Center: {tuple(center)}, Top Left: {topLeft}, Top Right: {topRight}, Bottom Left: {bottomLeft}, Bottom Right: {bottomRight} ")

"""We Plot all points found as the outermost corners. Each is marked from the previous section but also using color coded dotted plot lines cross-sectioned with teh same color. Originally, we would find the average point of a cluster of points but has since been repurposed, as we were able to use the Euclidean Distance to find the true corners."""

figure, axis = plt.subplots(1, 1)

axis.imshow(img)

axis.axhline([topLeft[0]], color='g', label='corner', linestyle='--')
axis.axhline([topRight[0]], color='b', label='corner', linestyle='--')
axis.axhline([bottomLeft[0]], color='purple', label='corner', linestyle='--')
axis.axhline([bottomRight[0]], color='orange', label='corner', linestyle='--')
axis.axhline([center[0]], color='r', label='center', linestyle='--')

axis.axvline([topLeft[1]], color='g', label='corner', linestyle='--')
axis.axvline([topRight[1]], color='b', label='corner', linestyle='--')
axis.axvline([bottomLeft[1]], color='purple', label='corner', linestyle='--')
axis.axvline([bottomRight[1]], color='orange', label='corner', linestyle='--')
axis.axvline([center[1]], color='r', label='center', linestyle='--')

figure.set_figheight(12)
figure.set_figwidth(12)

# load in the x and y from each point
width = 600
height = 400
# reverse tuple as it needs to be fed in as y due to the nature of 2d arrays
print(topLeft[::-1])
original_corners = np.float32([topLeft[::-1], topRight[::-1], bottomLeft[::-1], bottomRight[::-1]])
# pixel location of corners
new_corners = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
# create matrix needed for transforming to the new perspective
matrix = cv2.getPerspectiveTransform(original_corners, new_corners)
print(matrix)
result = cv2.warpPerspective(np.array(img), matrix, (width, height))
# plt.imshow(result)
# plt.axis('off')
# plt.show()
cv2.imshow(result)
