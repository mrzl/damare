import os

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

def buttonCallback():
    print(e.get())


def findLocalImageCallback():
    fname = askopenfilename(
        filetypes=(
            ("All files", "*.*"),
            ("Image files", "*.jpg;*.jpeg;*.png")
        ),
        initialdir=(os.path.expanduser('~/'))
    )
    if fname:
        try:
            e.delete(0, tk.END)
            e.insert(0, fname)
            e.pack(side="left")
        except:  # <- naked except is a bad idea
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

root = tk.Tk()

w = tk.Label(root, text="Hello Tkinter!")
w.pack()

e = tk.Entry(root)
e.pack(side="left")

e.delete(0, tk.END)
e.insert(0, "a default value")

b = tk.Button(root, text="run", command=buttonCallback)
b.pack()

b2 = tk.Button(root, text="local image", command=findLocalImageCallback)
b2.pack()

root.mainloop()