import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

import os
import sys

from fabric_helper import FabricHelper


class Window(object):
    def __init__(self):
        self.fabric = FabricHelper()

        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, width=100, height=100)

        self.topLabel = tk.Label(self.frame, text="黙れ—左", font=("Helvetica", 26))
        self.topLabel.pack()

        self.e = tk.Entry(self.frame, width=50)
        self.e.pack()

        self.e.delete(0, tk.END)
        self.e.insert(0, "/home/mar/Downloads/changi02.jpg")

        self.runButton = tk.Button(self.frame, text="走る (run)", command=self.button_cb)
        self.runButton.pack()

        self.imageButton = tk.Button(self.frame, text="画像 (image)", command=self.local_image_cb)
        self.imageButton.pack()

        self.log = tk.Text(self.frame, height=10, width=120)
        self.log.pack(side=tk.BOTTOM)
        self.root.bind("<Escape>", sys.exit)
        self.frame.pack()

        self.root.mainloop()

    def button_cb(self):
        print(self.e.get())
        self.log.insert(tk.END, self.fabric.uname() + "\n")
        self.log.pack()
        tk.Tk.update(self.root)
        self.log.insert(tk.END, self.fabric.python_v() + "\n")
        self.log.pack()
        tk.Tk.update(self.root)
        self.log.insert(tk.END, self.fabric.pip_v() + "\n")
        self.log.pack()
        tk.Tk.update(self.root)

    def local_image_cb(self):
        fname = askopenfilename(
            filetypes=(
                ("All files", "*.*"),
                ("Image files", "*.jpg;*.jpeg;*.png")
            ),
            initialdir=(os.path.expanduser('~/'))
        )
        if fname:
            try:
                self.e.delete(0, tk.END)
                self.e.insert(0, fname)
                self.e.pack()
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return
