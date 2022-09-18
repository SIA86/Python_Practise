from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import ImageTk, Image


root = Tk()
root.title('Yandex Market Parser')
root.geometry('640x480')
root.iconbitmap('title.ico')

frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root)
frame3 = ttk.Frame(root)
frame4 = ttk.Frame(root)

frame1.grid()
frame2.grid()
frame3.grid()
frame4.grid()
