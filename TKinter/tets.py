import tkinter as tk       

app = tk.Tk()

lbl1 = tk.Label(text="hello")
lbl1.grid()
lbl1.grid_forget()
app.mainloop()                          