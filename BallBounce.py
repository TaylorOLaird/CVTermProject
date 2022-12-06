from tkinter import *

# image, windowWidth, windowHeight, arrayOfLines
def MakeGame(image, windowWidth, windowHeight, arrayOfLines):
    root = Tk()
    root.title('Balls and Walls')
    root.geometry(f"{windowWidth}x{windowHeight}")
    width, height = 300, 200
    # create white canvas inside of frame
    canvas = Canvas(root, width=windowWidth, height=windowHeight, bg='white')
    canvas.pack(pady=20)

    canvas.create_line(0, 100, 300, 100, fill='red')

    root.mainloop()


MakeGame(0, 500, 500, 1)
