from PIL import Image
import numpy as np
import cv2
import math


def euclideanDistance(point1, center):
    return math.sqrt(sum((point1 - center) ** 2))


def findMaxCorner(points, center):
    Distances = []
    for coordinate in points:
        Distances.append(euclideanDistance(np.array(coordinate), center))

    position = np.argmax(Distances)
    return points[position]


def get_corners(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    # convert to gray for cornerHarris
    gray = np.float32(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # BGR point changes
    # anywhere the corner (local max of the grandient matrix) is present change the pixel to red
    corner_threshold = 0.01
    # for every set it to red if its over threshold
    colorCorners = 0, 0, 255
    frame[dst > corner_threshold * dst.max()] = [colorCorners]

    # get all the red pixels as these are corners
    locationX, locationY = np.where((frame == (colorCorners)).all(axis=2))

    # pairs thes x,y's together
    coordinates = [(locationX[i], locationY[i]) for i in range(len(locationX))]

    locationX = locationX if len(locationX) > 0 else [0]
    locationY = locationY if len(locationY) > 0 else [0]

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

    topLeft = findMaxCorner(topLeft, center) if len(
        topLeft) > 0 else (0, 0)

    topRight = findMaxCorner(topRight, center) if len(
        topRight) > 0 else (0, width)

    bottomLeft = findMaxCorner(bottomLeft, center) if len(
        bottomLeft) > 0 else (height, 0)

    bottomRight = findMaxCorner(bottomRight, center) if len(
        bottomRight) > 0 else (height, width)

    return frame, [topLeft, topRight, bottomLeft, bottomRight], (xDivision, yDivision)


def main():
    print(f"hello, world!")


if __name__ == "__main__":
    main()
