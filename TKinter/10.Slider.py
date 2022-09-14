from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk

def slide(var):
    
    lbl1['text'] = str(int(scl1.get()))
    lbl2['text'] = str(int(scl2.get()))
    lbl3['text'] = str(int(scl3.get()))

def mix():
    global imgTk
    imgTk = ImageTk.PhotoImage(Image.new(mode='RGB', size=(200, 200), color=(int(scl1.get()), int(scl2.get()), int(scl3.get()))))
    lbl_color['image'] = imgTk 
        

root = Tk()
root.title('Scale widget')

scl1 = ttk.Scale(root, from_=0, to=255, orient=VERTICAL, command=slide)
scl2 = ttk.Scale(root, from_=0, to=255, orient=VERTICAL, command=slide)
scl3 = ttk.Scale(root, from_=0, to=255, orient=VERTICAL, command=slide)

lbl11 = ttk.Label(root, text='Red')
lbl22 = ttk.Label(root, text='Green')
lbl33 = ttk.Label(root, text='Blue')
lbl1 = ttk.Label(root, text=scl1.get())
lbl2 = ttk.Label(root, text=scl2.get())
lbl3 = ttk.Label(root, text=scl3.get())


scl1.grid(column=0, row=2, padx=10, pady=5)
scl2.grid(column=1, row=2, padx=10, pady=5)
scl3.grid(column=2, row=2, padx=10, pady=5)
lbl1.grid(column=0, row=1)
lbl2.grid(column=1, row=1)
lbl3.grid(column=2, row=1)
lbl11.grid(column=0, row=0)
lbl22.grid(column=1, row=0)
lbl33.grid(column=2, row=0)

root2 = Toplevel()
root2.title('RGB color')

img = ImageTk.PhotoImage(Image.new(mode='RGB', size=(200, 200), color=(0, 0, 0)))
lbl_color = ttk.Label(root2, image=img, padding='10 10 10 0')
btn = ttk.Button(root2, text='MIX IT!', command=mix)


btn.grid(column=0, row=1, pady=10, padx=10)
lbl_color.grid(column=0, row=0)


root.lower(belowThis=root2)
root.mainloop()