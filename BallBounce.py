from tkinter import *
import numpy as np


# image, windowWidth, windowHeight, arrayOfLines
def MakeGame(image, windowWidth, windowHeight, arrayOfLines):
    root = Tk()
    root.title('Balls and Walls')
    root.geometry(f"{windowWidth}x{windowHeight}")
    width, height = 300, 200
    # create white canvas inside of frame
    canvas = Canvas(root, width=windowWidth, height=windowHeight, bg='white')
    canvas.pack(pady=20)
    # print(arrayOfLines)
    x, y = np.where(arrayOfLines == 0)
    for i in range(len(x)):
        # print(i)
        # np.where(x == 0)
        canvas.create_oval(x[i], y[i], x[i] + 3, y[i] + 3, fill='red')

    root.mainloop()


# MakeGame(0, 500, 500, 1)
