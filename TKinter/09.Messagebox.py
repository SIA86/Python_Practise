from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import ImageTk, Image

# showinfo, showwarning, showerrorm, askquestion, askokcancel, askyesno

LOGIN = 'Igor'
PASSWORD = '123'


def ask():
    messagebox.showwarning('Attension', 'All unsaved information will be lost!')
    response2 = messagebox.askyesno('Exit', 'Do you realy want to exit?')
    if response2 == 1:
        root2.quit()


def info_message():
    
    response = messagebox.askokcancel('Notification', 'Did you check everything and want to sign in?')
    if response == 1:
        if ent1.get()==LOGIN and ent2.get()==PASSWORD:
            messagebox.showinfo('Acces accept!', 'Welcome!')
            root.destroy()
            global root2
            root2 = Tk()
            
            global img
            img = ImageTk.PhotoImage(Image.open('Coco.jpg'))
            lbl3 = ttk.Label(root2, image=img)
            lbl3.grid(column=0, row=0)
            ttk.Button(root2, text="EXIT", command=ask).grid(column=0, row=0, sticky='s')
            root2.mainloop
        else:
            messagebox.showerror('Acces denied!', 'Wrong login or password')
            ent1.delete(0, END)
            ent2.delete(0, END)
            
            
    

root = Tk()
root.title('Sign In')
frm1 = ttk.Frame(root, padding='10 5 10 2')
ent1 = ttk.Entry(frm1, width=30)
ent1.focus_set()
ent2 = ttk.Entry(frm1, width=30)
lbl1 = ttk.Label(frm1, text='Login')
lbl2 = ttk.Label(frm1, text='Password')
btn1 = ttk.Button(root, text='Sign In', command=info_message, width=10)

frm1.pack()
ent1.grid(column=1, row=0, padx=2, pady=5)
ent2.grid(column=1, row=1,  padx=2, pady=5)
lbl1.grid(column=0, row=0, sticky=E)
lbl2.grid(column=0, row=1, sticky=E)
btn1.pack(pady=10)

root.mainloop()