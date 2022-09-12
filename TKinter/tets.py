from tkinter import *
import tkinter.ttk as ttk
from turtle import width

root = Tk()

style = ttk.Style()
print(style.layout('TButton'))
print(style.lookup('Tbutton'))

button = ttk.Button(root, text="hello")

#print(button.configure().keys())


#root.mainloop()
