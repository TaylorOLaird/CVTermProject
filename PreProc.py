import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

CORNERS = []


def load_images_from_folder(dir):
    image_names = os.listdir(dir)
    image_list = []
    for png in image_names:
        image_list.append(Image.open(f"{dir}/{png}"))
    return image_names, image_list


def mouse_event(event):
    global CORNERS
    CORNERS.append((round(event.xdata), round(event.ydata)))


def get_corner(image):
    fig = plt.figure()
    # essentially use an event listener to send mouse clicks to a list
    cid = fig.canvas.mpl_connect('button_press_event', mouse_event)

    # show the image for you to click on
    plt.imshow(image)
    plt.axis('off')
    plt.show()


def main():
    # load in the images from a folder
    image_labels, image_list = load_images_from_folder("batches/0")

    # set up height/width vars based callibrate.png
    width, height = Image.open(f"callibrate.png").size

    # set up pand to store data for training a model later
    df = pd.DataFrame()

    for image in image_list:
        global CORNERS
        CORNERS.clear()

        # get the corners, we did it a little weird with the
        # global list so we could get all 4 clicks from 1 imshow
        get_corner(image)
        print(f"corner from mouse events: {CORNERS}")

        top_left = CORNERS[0]
        top_right = CORNERS[1]
        bottom_left = CORNERS[2]
        bottom_right = CORNERS[3]

        # load in the x and y from each point
        original_corners = np.float32([[top_left[0], top_left[1]],
                                       [top_right[0], top_right[1]],
                                       [bottom_left[0], bottom_left[1]],
                                       [bottom_right[0], bottom_right[1]]])

        new_corners = np.float32([[0, 0],
                                  [width, 0],
                                  [0, height],
                                  [width, height]])

        # generate the transformation matrix and prints it, just to let us know how we're
        # doing with tagging the corners as we go, and this will be similar to what the cnn
        # attempts to do later
        matrix = cv2.getPerspectiveTransform(original_corners, new_corners)
        result = cv2.warpPerspective(np.array(image), matrix, (width, height))
        plt.imshow(result)
        plt.axis('off')
        plt.show()

        new_row = pd.DataFrame(
            {'top_left_x': [top_left[0]], 'top_left_y': [top_left[1]],
             'top_right_x': [top_right[0]], 'top_right_y': [top_right[1]],
             'bottom_left_x': [bottom_left[0]], 'bottom_left_y': [bottom_left[1]],
             'bottom_right_x': [bottom_right[0]], 'bottom_right_y': [bottom_right[1]]})

        # add it to the main df
        df = pd.concat([df, new_row], axis=0, ignore_index=True)
        print(f"current df: {df}")

    # print df to terminal for debugging and also save to csv to train with later
    print(f"final df: {df}")
    df.to_csv('images_with_corners.csv', index=False)


if __name__ == "__main__":
    main()
