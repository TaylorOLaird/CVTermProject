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
        zoom = 0.5
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
        # cv2.imshow('Video feed', out_frame)

        # # store the current frame as last frame for later use
        # last_pil = im_pil
        # # probably will also need to save the current corners

        # im_h = cv2.hconcat([im1, im1])
        # cv2.imwrite('data/dst/opencv_hconcat.jpg', im_h)
        video_feed = np.copy(out_frame)
        corners, coorner_coords = CornerDetection.get_corners(
            np.copy(out_frame))
        true_corners = np.copy(out_frame)
        affine = np.copy(out_frame)

        # print(coorner_coords)
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

        # Line thickness of 8 px
        thickness = 2

        # Using cv2.polylines() method
        # Draw a Green polygon swith
        # thickness of 1 px
        true_corners = cv2.polylines(true_corners, [pts],
                                     isClosed, color,
                                     thickness)

        affine = do_affine(affine, coorner_coords)

        one_and_two = cv2.hconcat([video_feed, corners])
        three_and_four = cv2.hconcat([true_corners, affine])
        all_four = cv2.vconcat([one_and_two, three_and_four])

        # fullscreen = cv2.resize(all_four, (width*2, height*2))
        cv2.imshow('Feeds', all_four)

        # enter exits the program
        if cv2.waitKey(1) == 13:
            # pass image to be grayed and get thresholded image
            break
    # kill and close the window when we're done
    cap.release()
    cv2.destroyAllWindows()

    grayThreshold = LineThresholding.threshold(corners)
    BallBounce.MakeGame(corners, corners.shape[0], corners.shape[1], grayThreshold)

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
