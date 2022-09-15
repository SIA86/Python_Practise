from tkinter import *
import tkinter.ttk as ttk


def show():
    lbl1 = ttk.Label(root, text=clicked.get())
    lbl1.pack()

options = [
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday", 
    "Friday", 
    "Sturday", 
    "Sunday"
]
root = Tk()
root.title('Drop Menu')

clicked = StringVar()
clicked.set(options[0])

drop = ttk.OptionMenu(root, clicked, *options)
drop.pack()

btn1= ttk.Button(root, text="Show Selection", command=show)
btn1.pack()

root.mainloop()