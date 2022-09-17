from operator import ne
from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title('Notebook')
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

frm1 = ttk.Frame(notebook, width=480, height=240)
frm2 = ttk.Frame(notebook, width=480, height=240)

ttk.Label(frm1, text="hello").pack()
ttk.Separator(frm1).pack(fill=X)
ttk.Label(frm1, text="hello").pack()
ttk.Sizegrip(root).pack(anchor='ne')


frm1.pack(fill='both', expand=True)
frm2.pack(fill='both', expand=True)

notebook.add(frm1, text="Parser")
notebook.add(frm2, text="DataBase")

mainloop()