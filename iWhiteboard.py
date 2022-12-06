import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import CornerDetection


def do_affine(img, points):
    height = int(img.shape[0])
    width = int(img.shape[1])

    top_left = points[0]
    top_right = points[1]
    bottom_left = points[2]
    bottom_right = points[3]

    # load in the x and y from each point
    original_corners = np.float32([[top_left[1], top_left[0]],
                                   [top_right[1], top_right[0]],
                                   [bottom_left[1], bottom_left[0]],
                                   [bottom_right[1], bottom_right[0]]])

    new_corners = np.float32([[0, 0],
                              [width, 0],
                              [0, height],
                              [width, height]])

    # generate the transformation matrix and prints it, just to let us know how we're
    # doing with tagging the corners as we go, and this will be similar to what the cnn
    # attempts to do later
    matrix = cv2.getPerspectiveTransform(original_corners, new_corners)
    result = cv2.warpPerspective(np.array(img), matrix, (width, height))
    # plt.imshow(result)
    # plt.axis('off')
    # plt.show()
    return result


def main():
    primary_webcam = 0
    secondary_webcam = 1
    cap = cv2.VideoCapture(primary_webcam)
    # set it as first frame just so its the right format
    last_pil = cap.read()
    while True:
        _, img = cap.read()
        # print(img.shape)
        zoom = 0.45
        height = int(img.shape[0]*zoom)
        width = int(img.shape[1]*zoom)
        # convert the image into PIL for easier operations later
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        # do operations on the PIL
        im_pil = im_pil.crop((0, 0, width, height))

        # converts the PIL back into the right color space and array
        # so imshow can show it
        out_frame = cv2.cvtColor(np.array(im_pil), cv2.COLOR_RGB2BGR)

        # set up each feed
        ##################################################################
        # feed 1
        video_feed = np.copy(out_frame)
        ##################################################################
        ##################################################################
        # corners is feed 2
        corners, coorner_coords, division = CornerDetection.get_corners(
            np.copy(out_frame))
        ##################################################################

        ##################################################################
        # feed 3 is the cross from our threshold
        threshold_lines = np.copy(out_frame)
        yDivision, xDivision = division
        x_top = (xDivision, 0)
        x_sub = (xDivision, height)

        y_top = (0, yDivision)
        y_sub = (width, yDivision)

        cross_pts = np.array([[x_top[0], x_top[1]],
                              [x_sub[0], x_sub[1]]], np.int32)

        # [y_top[0], y_top[1]],
        #                       [y_sub[0], y_sub[1]]
        cross_pts = cross_pts.reshape((-1, 1, 2))
        cross_isClossed = False
        # Green color in BGR
        cross_color = (255, 0, 0)

        # Line thickness of 2 px
        thickness = 2

        # this only has virticle line
        threshold_lines = cv2.polylines(threshold_lines, [cross_pts],
                                        cross_isClossed, cross_color,
                                        thickness)
        cross_pts = np.array([[y_top[0], y_top[1]],
                              [y_sub[0], y_sub[1]]], np.int32)
        # it now has both lines
        threshold_lines = cv2.polylines(threshold_lines, [cross_pts],
                                        cross_isClossed, cross_color,
                                        thickness)
        ##################################################################

        ##################################################################
        # feed 4 is true_corners
        true_corners = np.copy(out_frame)
        affine = np.copy(out_frame)

        top_left = coorner_coords[0]
        top_right = coorner_coords[1]
        bottom_left = coorner_coords[2]
        bottom_right = coorner_coords[3]
        # # Polygon corner points coordinates
        pts = np.array([[top_left[1], top_left[0]],
                        [top_right[1], top_right[0]],
                        [bottom_right[1], bottom_right[0]],
                        [bottom_left[1], bottom_left[0]]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        isClosed = True
        # Green color in BGR
        color = (0, 255, 0)
        # Using cv2.polylines() method
        # Draw a Green polygon swith
        # thickness of 1 px
        true_corners = cv2.polylines(true_corners, [pts],
                                     isClosed, color,
                                     thickness)
        ##################################################################

        ##################################################################
        # feed 5
        affine = do_affine(affine, coorner_coords)
        ##################################################################

        one_to_three = cv2.hconcat([video_feed, corners, threshold_lines])
        four_to_six = cv2.hconcat([true_corners, affine, affine])
        all_six = cv2.vconcat([one_to_three, four_to_six])

        cv2.imshow('Feeds', all_six)

        # enter exits the program
        if cv2.waitKey(1) == 13:
            break
    # kill and close the window when we're done
    cap.release()
    cv2.destroyAllWindows()

    # # display last_pil
    # plt.imshow(np.asarray(last_pil))
    # plt.axis('off')
    # plt.show()

    # # display last_pil with affine
    # plt.imshow(
    #     do_affine(last_pil, [(0, 0), (300, 0), (0, 300), (300, 300)]))
    # # probably save this as pdf in final product
    # plt.axis('off')
    # plt.show()


if __name__ == "__main__":
    main()
