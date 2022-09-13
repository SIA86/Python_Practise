from tkinter import *
import tkinter.ttk as ttk
# showinfo, showwarning, showerrorm, askquestion, askokcancel, askyesno

root = Tk()
root.title('Sign In')
frm1 = ttk.Frame(root, padding='10 5 10 2')
ent1 = ttk.Entry(frm1, width=30)
ent2 = ttk.Entry(frm1, width=30)
lbl1 = ttk.Label(frm1, text='Login')
lbl2 = ttk.Label(frm1, text='Password')
btn1 = ttk.Button(root, text='Sign In', command=None, width=10)

frm1.pack()
ent1.grid(column=1, row=0, padx=2, pady=5)
ent2.grid(column=1, row=1,  padx=2, pady=5)
lbl1.grid(column=0, row=0, sticky=E)
lbl2.grid(column=0, row=1, sticky=E)
btn1.pack(pady=10)

root.mainloop()