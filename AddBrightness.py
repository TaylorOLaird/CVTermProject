import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import skimage
import pandas as pd
from PIL import Image


def load_image(dir, image_name):
    return Image.open(f"{dir}/{image_name}")


def main():
    batch = 0
    in_df = pd.read_csv(f"noise_label_matrix.csv")
    print(f"in_df: \n{in_df}")
    batch_siz = len(in_df)
    print(f"batch_siz: {batch_siz}")

    # set up panda to store data for training a model later
    out_df = pd.DataFrame()
    print(f"out_df: \n{out_df}")

    # Change the current working directory
    os.chdir(os.getcwd() + "/noise_images")
    print(f"getcwd: {os.getcwd()}")
    for i in range(batch_siz):
        current_label = in_df["image_label"].iloc[i]
        noises = ["poisson", "s&p", "none"]
        for noise in noises:
            # generate the apropriat label
            new_label = f"{noise}_{current_label}" if noise != "none" else current_label
            # grab the current row, and replace the label for the xy values with the apropriate
            # new label, then concatinate with the main df
            new_row = pd.DataFrame(data=in_df.iloc[i].replace(
                current_label, new_label).values)
            out_df = pd.concat([out_df, new_row], axis=1, ignore_index=True)

            # load the image
            current_image = load_image(f"../batches/{batch}", current_label)
            # genereate the image with noise
            image_with_noise = skimage.util.random_noise(
                np.asarray(current_image), noise) if noise != "none" else current_image
            # save the image, notice right now we're in /noise_images
            plt.imsave(new_label, image_with_noise)

    # leave the photos folder
    os.chdir('../')

    # transpose the df
    out_df = out_df.T
    # fix the names for the cols
    out_df.columns = ["image_label",
                      "top_left_x", "top_left_y",
                      "top_right_x", "top_right_y",
                      "bottom_left_x", "bottom_left_y",
                      "bottom_right_x", "bottom_right_y"]
    print(out_df)

    # save data
    out_df.to_csv('noise_label_matrix.csv', index=False)


if __name__ == "__main__":
    main()
