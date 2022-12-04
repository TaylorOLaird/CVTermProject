import os
from PIL import Image


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        current_image = Image.open(os.path.join(folder, filename))
        images.append(current_image)
    return images


def main():
    frames = load_images_from_folder("VideoFrames")
    print(len(frames))

    os.chdir(os.getcwd() + "/batches")
    current_batch = 0
    frame_per_batch = 40

    for i in range(0, len(frames), frame_per_batch):
        # make and go into batch folder
        path = f"{os.getcwd()}/{current_batch}"
        os.mkdir(path)
        os.chdir(path)

        # add images in the folder
        for j in range(i, i + frame_per_batch):
            frames[j].save(f"{j}_frame.png")

        # leave the current batch folder
        os.chdir('../')
        current_batch += 1
    # leave batches folder
    os.chdir('../')


if __name__ == "__main__":
    main()
