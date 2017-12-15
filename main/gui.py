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

        self.sync_images()

        self.event_loop = asyncio.new_event_loop()
        sync_task = self.event_loop.create_task(self.sync_images())

        self.root = tk.Tk()
        self.root.title('黙れ—左')
        self.root.bind("<Escape>", self.quit)

        self.topLabel = tk.Label(self.root, text="黙れ—左", font=("Helvetica", 26)).grid(row=0, column=0, columnspan=3)

        # topic for the train section
        self.train_topic = tk.Label(self.root, text="train").grid(row=1, column=0)

        # line to select the host
        self.host_label = tk.Label(self.root, text="host").grid(row=2, column=0)
        self.host_entry = tk.Entry(self.root)
        self.host_entry.grid(row=2, column=1)
        self.host_entry.delete(0, tk.END)
        self.host_entry.insert(0, self.lyrik.host)

        # line to select the style file itself
        self.style_label = tk.Label(self.root, text="style").grid(row=3, column=0)
        self.selected_style = tk.StringVar(self.root)
        self.selected_style.set('choose')
        self.styles_chooser = tk.OptionMenu(self.root, self.selected_style, *self.lyrik.style_images()).grid(row=3, column=1)

        # line to select the image size for the training
        self.image_size_label = tk.Label(self.root, text="image size").grid(row=4, column=0)
        self.image_size_entry = tk.Entry(self.root)
        self.image_size_entry.grid(row=4, column=1)
        self.image_size_entry.delete(0, tk.END)
        self.image_size_entry.insert(0, 1080)

        # line to select the content weight for the training
        self.content_weight_label = tk.Label(self.root, text="content weight").grid(row=5, column=0)
        self.content_weight_entry = tk.Entry(self.root)
        self.content_weight_entry.grid(row=5, column=1)
        self.content_weight_entry.delete(0, tk.END)
        self.content_weight_entry.insert(0, 1.0)

        # line to select the style weight for the training
        self.style_weight_label = tk.Label(self.root, text="style weight").grid(row=6, column=0)
        self.style_weight_entry = tk.Entry(self.root)
        self.style_weight_entry.grid(row=6, column=1)
        self.style_weight_entry.delete(0, tk.END)
        self.style_weight_entry.insert(0, 5.0)

        def train():
            style_image = self.selected_style.get()
            style_size = self.image_size_entry.get()
            content_weight = self.content_weight_entry.get()
            style_weight = self.style_weight_entry.get()
            self.lyrik.train(style_image, style_size, content_weight, style_weight)

        # train button
        self.train_button = tk.Button(self.root, text='train!', command=train).grid(row=7, column=2)


        #self.e = tk.Entry(self.frame, width=50)

        #self.e.delete(0, tk.END)
        #self.e.insert(0, "/home/mar/Downloads/changi02.jpg")

        #self.runButton = tk.Button(self.frame, text="走る (run)", command=self.button_cb)

        #self.imageButton = tk.Button(self.frame, text="画像 (image)", command=self.local_image_cb)

        #model_files = self.lyrik.models()

        #self.selected_model_file = tk.StringVar(self.frame)
        #self.selected_model_file.set('Choose Model')  # default value

        #self._models = tk.OptionMenu(self.frame, self.selected_model_file, *model_files)

        #self.modelButton = tk.Button(self.frame, text="型 (model)", command=self.check_model)

        #self.log = tk.Text(self.frame, height=10, width=120)

        self.root.mainloop()

    def quit(self, ev):
        self.lyrik.disconnect()
        self.event_loop.close()
        sys.exit(0)

    def button_cb(self):
        #print(self.e.get())
        #self.log.insert(tk.END, self.lyrik.uname() + "\n")
        #self.log.pack()
        #tk.Tk.update(self.root)
        #self.log.insert(tk.END, self.lyrik.python_version() + "\n")
        #self.log.pack()
        #tk.Tk.update(self.root)
        #self.log.insert(tk.END, self.lyrik.pip_version() + "\n")
        #self.log.pack()
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

        if self.lyrik.fabric.ERROR in lyrik_images:
            print('Not syncing, no connection to Lyrik.')
            return

        local_images = self.local.style_images()

        lyrik_missing = list(set(local_images) - set(lyrik_images))

        lyrik_missing = [os.path.join(self.local.images_folder, fn) for fn in lyrik_missing]

        self.lyrik.upload(self.lyrik.style_images_folder, lyrik_missing)
