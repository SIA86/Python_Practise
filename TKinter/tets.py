import tkinter as tk  
from tkinter import Label, filedialog   
from PIL import Image, ImageTk  

root = tk.Tk()
root.filename = filedialog.askopenfilename(initialdir=r'C:\Users\Igor\Documents\Python', 
                                           title='some title', 
                                           filetypes=(('png files', '*.png'),
                                           ('jpg files', '*.jpg')))

my_img = ImageTk.PhotoImage(Image.open(root.filename))
lbl1 = tk.Label(root, image=my_img)
lbl1.pack()


root.mainloop()                 