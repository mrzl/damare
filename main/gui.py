import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

import os
import sys

import asyncio

from lyrik import Lyrik
from local import Local


class Window(object):
    def __init__(self):
        self.lyrik = Lyrik()
        self.local = Local()

        #self.sync_images()

        self.event_loop = asyncio.get_event_loop()
        sync_task = self.event_loop.create_task(self.sync_images())
        self.event_loop.run_until_complete(sync_task)

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

        model_files = self.lyrik.models()

        self.selected_model_file = tk.StringVar(self.frame)
        self.selected_model_file.set(model_files[0])  # default value

        self._models = tk.OptionMenu(self.frame, self.selected_model_file, *model_files)
        self._models.pack()

        self.modelButton = tk.Button(self.frame, text="型 (model)", command=self.check_model)
        self.modelButton.pack()

        self.log = tk.Text(self.frame, height=10, width=120)
        self.log.pack(side=tk.BOTTOM)
        self.root.bind("<Escape>", self.quit)
        self.frame.pack()

        self.root.mainloop()

    def quit(self, ev):
        self.lyrik.disconnect()
        self.event_loop.close()
        sys.exit(0)

    def button_cb(self):
        print(self.e.get())
        self.log.insert(tk.END, self.lyrik.uname() + "\n")
        self.log.pack()
        tk.Tk.update(self.root)
        self.log.insert(tk.END, self.lyrik.python_version() + "\n")
        self.log.pack()
        tk.Tk.update(self.root)
        self.log.insert(tk.END, self.lyrik.pip_version() + "\n")
        self.log.pack()
        tk.Tk.update(self.root)

    def check_model(self):
        print(self.selected_model_file.get())

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

    async def sync_images(self):
        lyrik_images = self.lyrik.style_images()
        local_images = self.local.style_images()

        lyrik_missing = list(set(local_images) - set(lyrik_images))

        lyrik_missing = [os.path.join(self.local.images_folder, fn) for fn in lyrik_missing]

        self.lyrik.upload(self.lyrik.style_images_folder, lyrik_missing)
