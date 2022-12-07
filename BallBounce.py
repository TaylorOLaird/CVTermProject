from tkinter import *
import numpy as np


# image, windowWidth, windowHeight, arrayOfLines
def MakeGame(image, windowWidth, windowHeight, arrayOfLines):
    root = Tk()
    root.title('Balls and Walls')
    root.geometry(f"{windowWidth * 2}x{windowHeight * 2}")
    # create white canvas inside of frame
    canvas = Canvas(root, width=windowWidth, height=windowHeight, bg='white')
    canvas.pack()
    x, y = np.where(arrayOfLines == 255)
    for i in range(len(x)):
        canvas.create_rectangle(y[i], x[i], y[i] + 3, x[i] + 3, fill='red')

    class Ball:
        def __init__(self, size, color):
            self.ball = canvas.create_oval(0, 0, size, size, fill=color)
            self.speedx = 4
            self.speedy = 4
            self.movement()

        def movement(self):
            canvas.move(self.ball, self.speedx, self.speedy)
            # return list of coordinates of shape
            pos = canvas.coords(self.ball)
            if pos[2] >= windowWidth or pos[0] <= 0:
                self.speedx *= -1
            if pos[3] >= windowHeight or pos[1] <= 0:
                self.speedy *= -1
            root.after(40, self.movement)

    ball = Ball(10, 'brown')

    root.mainloop()
