import tkinter as tk
from tkinter import ttk
import random

def roll():
    lbl_value["text"] = str(random.randint(1, 6))

window = tk.Tk()

window.rowconfigure([0, 1], minsize=50, weight=1)
window.columnconfigure(0, minsize=50, weight=1)

btn_roll = ttk.Button(master=window, text="Roll", command=roll)
btn_roll.grid(row=0, column=0, sticky="nsew")

lbl_value = ttk.Label(master=window, text="0")
lbl_value.grid(row=1, column=0)

window.mainloop()