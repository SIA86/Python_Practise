from tkinter import *
import tkinter.ttk as ttk


root = Tk()
root.title('Pizza Prices')
root.iconbitmap('favicon.ico')



pizza= StringVar()
pizza.set(None)


TOPPING = [("Pepperony", "10.50$"),
            ("Mushroom", "9.85$"),
            ("Vegetables", "8.50$"),
            ("Meet", "12.99$"),
            ("Fish", "15.00$")]

for name, price in TOPPING:
    Radiobutton(root, text=name, variable=pizza, value=price, command=lambda: show_price(pizza.get())).grid(sticky=W)

lbl1 = ttk.Label(root, text="0.00$", font=36)
lbl1.grid(padx=10, pady=10)

def show_price(price):
    lbl1['text'] = price
    

root.mainloop()