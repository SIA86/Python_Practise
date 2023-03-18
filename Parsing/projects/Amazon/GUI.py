from tkinter import *
import tkinter.ttk as ttk
import os

#GUI commands

def check_time_on():
    if S_timeout.get() == 1:
        ent_time.configure(state=NORMAL)
    else:
        ent_time.configure(state=DISABLED)

def check_multy_on():
    if S_multy.get() == 1:
        ent_multy.configure(state=NORMAL)
    else:
        ent_multy.configure(state=DISABLED)

#Create GUI

root = Tk()
root.title('Amazon Market Parser')
root.resizable(width=False, height=False)

#Create parent frame - Frame 1
frame1 = ttk.Frame(root, borderwidth=5, relief='sunken', padding='0 5 0 5')
frame1.grid(column=0, row=0, sticky=W+E)

#Create child frame - Frame 2
frame2 = ttk.Frame(frame1)
frame2.grid(column=0, row=0)

ent_url = ttk.Entry(frame2, width=80)
lbl_ent_url = ttk.Label(frame2, text='URL:')
lbl_notation = ttk.Label(frame2, text='Choose the product what you are looking for and set all filter you need \nthan copy the link from your browser to the field above')
ttk.Separator(frame2).grid(row=2, columnspan=2, sticky=E+W, pady=5)

ent_url.grid(column=1, row=0, padx=5)
lbl_ent_url.grid(column=0, row=0, padx=5)
lbl_notation.grid(column=1, row=1, padx=5)

#Create child frame - Frame 3
frame3 = ttk.Frame(frame1)
frame3.grid(column=0, row=1, sticky=W+E)

#First column (filter options: name, price, articul, marka)
name = BooleanVar()
price = BooleanVar()
art = BooleanVar()
mark = BooleanVar()
name.set(0)
price.set(0)
art.set(0)
mark.set(0)

lbl_ch_filter = ttk.Label(frame3, text='Choose filter:')
ch_name = ttk.Checkbutton(frame3, text='Name', variable=name)
ch_price = ttk.Checkbutton(frame3, text='Price', variable=price)
ch_art = ttk.Checkbutton(frame3, text='Art', variable=art)
ch_mark = ttk.Checkbutton(frame3, text='Mark', variable=mark)

lbl_ch_filter.grid(column=0, row=0, sticky=W, padx=5, pady=2)
ch_name.grid(column=0, row=1, sticky=W, padx=5, pady=2)
ch_price.grid(column=0, row=2, sticky=W, padx=5, pady=2)
ch_art.grid(column=0, row=3, sticky=W, padx=5, pady=2)
ch_mark.grid(column=0, row=4, sticky=W, padx=5, pady=2)

#Second column (parser options)
S_timeout = IntVar()
S_proxy = IntVar()
S_multy = IntVar()
S_timeout.set(0)
S_proxy.set(0)
S_multy.set(0)

lbl_parser_options = ttk.Label(frame3, text='Parser options:', padding='50 0 0 0')
ch_proxy = ttk.Checkbutton(frame3, text='Use proxy', variable=S_proxy, padding='50 0 0 0')
ch_time = ttk.Checkbutton(frame3, text='Timeout', variable=S_timeout, command=check_time_on, padding='50 0 0 0')
ch_multy = ttk.Checkbutton(frame3, text='Multiprocessing', variable=S_multy, command=check_multy_on, padding='50 0 0 0')
ent_time = ttk.Entry(frame3, width=5, state=DISABLED)
ent_multy = ttk.Entry(frame3, width=5, state=DISABLED)

lbl_parser_options.grid(column=1, row=0, sticky=W, padx=5, pady=2)
ch_proxy.grid(column=1, row=1, sticky=W,  padx=5, pady=2)
ch_time.grid(column=1, row=2, sticky=W,  padx=5, pady=2)
ch_multy.grid(column=1, row=3, sticky=W,  padx=5, pady=2)
ent_time.grid(column=2, row=2, sticky=W, padx=5, pady=2)
ent_multy.grid(column=2, row=3, sticky=W,  padx=5, pady=2)

#Third column options
format = StringVar()

lbl_output_options = ttk.Label(frame3, text='Output format:')
rad_csv = ttk.Radiobutton(frame3, text='CSV', variable=format, value='csv')
rad_db = ttk.Radiobutton(frame3, text='SQL', variable=format, value='db')
rad_xls = ttk.Radiobutton(frame3, text='XLSX', variable=format, value='xlsx')

lbl_output_options.grid(column=3, row=0, sticky=W, padx=5, pady=2)
rad_csv.grid(column=3, row=1, sticky=W, padx=5, pady=2)
rad_db.grid(column=3, row=2, sticky=W, padx=5, pady=2)
rad_xls.grid(column=3, row=3, sticky=W, padx=5, pady=2)

#Create frame for buttons - Frame 4
frame4 = ttk.Frame(root)
frame4.grid(column=0, row=2, sticky=E)

btn1 = ttk.Button(frame4, text='Start', command=lambda:os.system('python WithPOOL.py'))
btn2 = ttk.Button(frame4, text='Exit', command=root.quit)

btn1.grid(column=0, row=0, padx=5, sticky=E)
btn2.grid(column=1, row=0, padx=5, sticky=E)

frame4.grid(column=0, row=2, sticky=E)

root.mainloop()

