import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import CornerDetection
import BallBounce
import LineThresholding


corners = 0


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
    return result


def main():
    primary_webcam = 0
    secondary_webcam = 1
    cap = cv2.VideoCapture(primary_webcam)
    # set it as first frame just so it's the right format
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

        true_corners = cv2.polylines(true_corners, [pts],
                                     isClosed, color,
                                     thickness)
        ##################################################################

        ##################################################################
        # feed 5
        affine = do_affine(affine, coorner_coords)
        ##################################################################

        ##################################################################
        # feed 6
        canny_feed = np.copy(affine)
        gray_canny_feed = cv2.cvtColor(canny_feed, cv2.COLOR_RGB2GRAY)
        blur_canny_feed = cv2.GaussianBlur(gray_canny_feed, (5, 5), 0)
        canny_data = cv2.Canny(blur_canny_feed, 90, 120)
        ret, canny_feed_mask = cv2.threshold(
            canny_data, 70, 255, cv2.THRESH_BINARY)
        # cv2.imshow('Video feed', mask)
        canny_feed_mask = cv2.cvtColor(canny_feed_mask, cv2.COLOR_GRAY2BGR)
        ##################################################################

        # horizontalling concatinate each feed then virticle concat them
        one_to_three = cv2.hconcat([video_feed, corners, threshold_lines])
        four_to_six = cv2.hconcat([true_corners, affine, canny_feed_mask])
        all_six = cv2.vconcat([one_to_three, four_to_six])

        cv2.imshow('Feeds', all_six)

        # enter exits the program
        if cv2.waitKey(1) == 13:
            # pass image to be grayed and get thresholded image
            break
    # kill and close the window when we're done
    cap.release()
    cv2.destroyAllWindows()

    # grayThreshold = LineThresholding.threshold(affine)
    gray = cv2.cvtColor(affine, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 90, 120)
    ret, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
    cv2.imshow('Video feed', mask)
    BallBounce.MakeGame(affine, affine.shape[1], affine.shape[0], mask)

    # save the affine as a pdf
    pil_affine = cv2.cvtColor(affine, cv2.COLOR_BGR2RGB)
    pil_affine = Image.fromarray(pil_affine)
    pil_affine.save("out.pdf")


if __name__ == "__main__":
    main()
