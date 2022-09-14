from tkinter import *
import tkinter.ttk as ttk


def button_click(number):
    current = entry.get()
    entry.delete(0, END)
    entry.insert(0, current + number)


def button_clear():
    entry.delete(0, END)


def button_action(button_name):
    global first_number
    first_number = float(entry.get())
    global action 
    action = button_name['text']
    entry.delete(0, END)


def button_equal():
    second_number = float(entry.get())
    entry.delete(0, END)
    
    if action == '+':
        entry.insert(0, first_number + second_number)
    if action == '-':
        entry.insert(0, first_number - second_number)
    if action == '/':
        entry.insert(0, first_number / second_number)
    if action == '*':
        entry.insert(0, first_number * second_number)


root = Tk()
root.title('Calculator')
root.resizable(width=False, height=False)

entry = ttk.Entry(root, justify="right")
entry.grid(column=0, row=0, columnspan=4, padx=2, pady=2, sticky="we")

button1 = ttk.Button(root, text='1', padding='5 10', command=lambda: button_click('1'))
button2 = ttk.Button(root, text='2', padding='5 10', command=lambda: button_click('2'))
button3 = ttk.Button(root, text='3', padding='5 10', command=lambda: button_click('3'))
button4 = ttk.Button(root, text='4', padding='5 10', command=lambda: button_click('4'))
button5 = ttk.Button(root, text='5', padding='5 10', command=lambda: button_click('5'))
button6 = ttk.Button(root, text='6', padding='5 10', command=lambda: button_click('6'))
button7 = ttk.Button(root, text='7', padding='5 10', command=lambda: button_click('7'))
button8 = ttk.Button(root, text='8', padding='5 10', command=lambda: button_click('8'))
button9 = ttk.Button(root, text='9', padding='5 10', command=lambda: button_click('9'))
button0 = ttk.Button(root, text='0', padding='5 10', command=lambda: button_click('0'))
button_add = ttk.Button(root, text='+', padding='5 10', command=lambda: button_action(button_add))
button_sub = ttk.Button(root, text='-', padding='5 10', command=lambda: button_action(button_sub))
button_div = ttk.Button(root, text='/', padding='5 10', command=lambda: button_action(button_div))
button_mult = ttk.Button(root, text='*', padding='5 10', command=lambda: button_action(button_mult))

button_eq = ttk.Button(root, text='=', padding='5 10', command=button_equal)
button_cl = ttk.Button(root, text='Clear', padding='5 10', command=button_clear)

button1.grid(column=0, row=1)
button2.grid(column=1, row=1)
button3.grid(column=2, row=1)
button_add.grid(column=3, row=1)

button4.grid(column=0, row=2)
button5.grid(column=1, row=2)
button6.grid(column=2, row=2)
button_sub.grid(column=3, row=2)

button7.grid(column=0, row=3)
button8.grid(column=1, row=3)
button9.grid(column=2, row=3)
button_div.grid(column=3, row=3)

button_cl.grid(column=0, row=4)
button0.grid(column=1, row=4)
button_eq.grid(column=2, row=4)
button_mult.grid(column=3, row=4)

root.mainloop()