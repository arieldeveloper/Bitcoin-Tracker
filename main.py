#Import Tkinter
import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)

#Main
class BitcoinTracker(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default = "icon.ico")
        tk.Tk.wm_title(self, "bitcoin tracker")
        container = tk.Frame(self)
        container.pack(side = "right", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for f in (StartPage, PageOne, PageTwo):

            frame = f(container, self)

            self.frames[f] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]

        #Raises the frame to the front
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Visit Page 1", command = lambda: controller.show_frame(PageOne))
        button1.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "Page One", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "back to home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

        button1 = ttk.Button(self, text="Page 2", command=lambda: controller.show_frame(PageTwo))
        button1.pack()

    tk.Frame

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "Page Two", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)


        button1 = ttk.Button(self, text = "back to home", command = lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="To page 1", command=lambda: controller.show_frame(PageOne))
        button2.pack()

    tk.Frame

app = BitcoinTracker()
app.mainloop()