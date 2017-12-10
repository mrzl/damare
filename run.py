import os, sys

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from fabric.api import run, cd, env
from fabric.context_managers import settings, hide
from fabric.network import disconnect_all


class FabricHelper(object):
    def __init__(self):
        self._host = "marcel@lyrik.ddns.net"
        self._key = "/home/mar/.ssh/id_rsa_marchi"

    def test(self):
        returnStrings = []
        env.host_string = self._host
        env.key_filename = self._key

        home_dir = "/home/marcel/fabric"
        with cd(home_dir):
            returnStrings.append(run("uname -a"))

            returnStrings.append(run("python -V"))
            returnStrings.append(run("pip -V"))

        disconnect_all()
        return returnStrings

    def capture(self):
        with settings(hide('running', 'commands', 'stdout', 'stderr')):
            stdout = execute(self.parallel_exec, hosts=self.hosts)
        return stdout


class Window(object):
    def __init__(self):
        self.fabric = FabricHelper()

        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, width=100, height=100)

        self.topLabel = tk.Label(self.frame, text="だまれ")
        self.topLabel.pack()

        self.e = tk.Entry(self.frame)
        self.e.pack()

        self.e.delete(0, tk.END)
        self.e.insert(0, "a default value")

        self.runButton = tk.Button(self.frame, text="run", command=self.button_cb)
        self.runButton.pack()

        self.imageButton = tk.Button(self.frame, text="image", command=self.local_image_cb)
        self.imageButton.pack()

        self.log = tk.Text(self.frame, height=10, width=120)
        self.log.pack(side=tk.BOTTOM)
        self.root.bind("<Escape>", sys.exit)
        self.frame.pack()

        self.root.mainloop()

    def button_cb(self):
        print(self.e.get())
        logs = self.fabric.test()
        for log in logs:
            print(log)
            self.log.insert(tk.END, log + "\n")
            self.log.pack()

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
                self.e.pack(side="left")
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return


if __name__ == '__main__':
    window = Window()
