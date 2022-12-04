# import cv2
# import numpy as np
import os
# import matplotlib.pyplot as plt
# import pandas as pd
from PIL import Image

# IMAGE_LABELS = []
CORNERS = []


def load_images_from_folder(dir):
    image_names = os.listdir(dir)
    image_list = []
    for png in image_names:
        # os.path.join(dir, image_name)
        image_list.append(Image.open(f"{dir}/{png}"))
    return image_names, image_list


# XCOORDINATES = []
# YCOORDINATES = []

# def mouse_event(event):
#     global XCOORDINATES
#     global YCOORDINATES
#     XCOORDINATES.append(round(event.xdata))
#     YCOORDINATES.append(round(event.ydata))
#     return


# def init_coords(image):
#     fig = plt.figure()
#     # essentially use an event listener to send mouse clicks to a list
#     cid = fig.canvas.mpl_connect('button_press_event', mouse_event)

#     # show the image for you to click on
#     plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     plt.axis('off')
#     plt.show()


def main():
    # load in the images from a folder
    image_labels, image_list = load_images_from_folder("batches/0")
    # print(image_labels)
    # print()
    # print(image_list)

    # set up height/width vars based on a ratio
    # 874/1200
    width = 1200
    height = 874

    # global XCOORDINATES
    # global YCOORDINATES
    global CORNERS

    # # set up pand to store data for training a model later
    # df = pd.DataFrame()

    # for index in range(len(images)):
    #     print(f"on iteration: {index}")
    #     # clear the coordinats list for the next image
    #     XCOORDINATES.clear()
    #     YCOORDINATES.clear()

    #     image = images[index]
    #     init_coords(image)

    #     if len(XCOORDINATES) > 4 or len(YCOORDINATES) > 4:
    #         print("generic useless error message: 159614895")
    #         break

    #     # do affine and metric rectification
    #     original_corners = np.float32([[XCOORDINATES[0], YCOORDINATES[0]], [XCOORDINATES[1], YCOORDINATES[1]], [
    #         XCOORDINATES[2], YCOORDINATES[2]], [XCOORDINATES[3], YCOORDINATES[3]]])
    #     # these will need to be set to the same ratio we draw the outline box in, since this is what we are
    #     # basically take where it is with the original, and morph it to these
    #     new_corners = np.float32(
    #         [[0, 0], [width, 0], [0, height], [width, height]])
    #     # generate the transformation matrix
    #     matrix = cv2.getPerspectiveTransform(original_corners, new_corners)
    #     print(matrix)

    #     # create a new row df
    #     new_row = pd.DataFrame({'image_label': [IMAGE_LABELS[index]], '0': [matrix[0][0]], '1': [matrix[0][1]], '2': [matrix[0][2]],
    #                             '3': [matrix[1][0]], '4': [matrix[1][1]], '5': [matrix[1][2]],
    #                             '6': [matrix[2][0]], '7': [matrix[2][1]], '8': [matrix[2][2]]})
    #     # add it to the main df
    #     df = pd.concat([df, new_row], axis=0, ignore_index=True)

    #     # again the dims here need to match the new corners
    #     result = cv2.warpPerspective(image, matrix, (width, height))

    #     # show the result of affine and rectification on the image with the matrix
    #     plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    #     plt.axis('off')
    #     plt.show()
    # # print df to terminal for debugging and also save to csv to train with later
    # print(df)
    # df.to_csv('label_matrix.csv', index=False)


if __name__ == "__main__":
    main()
