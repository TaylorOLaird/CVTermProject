import cv2
import numpy as np


def threshold(result):
    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    gray_image = np.where(gray_image > 130, 255, 0)
    return gray_image


