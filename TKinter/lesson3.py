from tkinter import *
import tkinter.ttk as ttk


field_names = ['First Name', 'Last Name', 'Adress Line 1', 'Adress Line 2', 'City', 'State/Province', 'Postal Code', 'Country'] 

root = Tk()
root.title('Adress Entry Form')
#root.geometry('600x300')


frm1 = ttk.Frame(root, relief="sunken", borderwidth=2, padding=2)
frm2 = ttk.Frame(root)
frm1.grid(column=0, row=0, sticky='nsew')
frm2.grid(column=0, row=1, sticky='e')

for row in range(len(field_names)):
    ttk.Label(frm1, text=field_names[row]).grid(column=0, row=row, sticky='e')
    ttk.Entry(frm1, width=50).grid(column=1, row=row)
    
ttk.Button(frm2, text='Clear').grid(column=0, row=0, padx=5, pady=5)
ttk.Button(frm2, text='Submit').grid(column=1, row=0, padx=5, pady=5)

root.mainloop()