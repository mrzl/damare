import os, sys

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from fabric.api import run, cd, env, execute
from fabric.context_managers import settings, hide
from fabric.network import disconnect_all

import configparser

class FabricHelper(object):
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read("settings.ini")

        self._host =cfg.get("lyrik", "host")
        self._key = cfg.get("lyrik", "key")
        self._home_dir = cfg.get("lyrik", "home_dir")
        self._password = cfg.get("lyrik", "password")

        env.host_string = self._host
        env.key_filename = self._key
        env.password = self._password
        #with cd(self._home_dir):

    def uname(self):
        return run("uname -a")

    def python_v(self):
        return run("python -V")

    def pip_v(self):
        return run("pip -V")

    def disconnect(self):
        disconnect_all()

    def capture(self):
        pass
        #with settings(hide('running', 'commands', 'stdout', 'stderr')):
        #    stdout = execute(self.parallel_exec, hosts=self.hosts)
        #return stdout


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


if __name__ == '__main__':
    window = Window()
