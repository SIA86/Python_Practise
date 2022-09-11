from tkinter import *
import tkinter.ttk as ttk


root = Tk()
frm = ttk.Frame()
entry = ttk.Entry(master=frm, background='white', foreground='black', width=40)
entry.pack()
entry.insert(0, "What is your name?")
frm.pack()

root.mainloop()