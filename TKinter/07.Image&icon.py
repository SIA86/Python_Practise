from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image

root = Tk()
root.title('Application with ICO')
root.iconbitmap('favicon.ico')
my_img = ImageTk.PhotoImage(Image.open('Coco.jpg'))

button_exit = ttk.Button(root, image=my_img, command=root.quit)
button_exit.grid(column=0, row=0)


img2 = PhotoImage(file='image1.gif')
lbl2 = ttk.Label(root, image=img2)
lbl2.grid(column=1, row=0)

root.mainloop()