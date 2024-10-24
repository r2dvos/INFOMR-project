import vedo
import tkinter as tk
from tkinter import filedialog

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button
import numpy as np
import shutil

class VedoOpener:
    already_open = False

    def open(self, event):
        if self.already_open == False:
            self.already_open = True
            mesh = vedo.Mesh(objFile)
            vedo.show(mesh, axes=0)
            self.already_open = False

shutil.rmtree('./temp_images', ignore_errors=True)
Path("./temp_images").mkdir(parents=True, exist_ok=True)

root = tk.Tk()
root.withdraw()

objFile = filedialog.askopenfilename(initialdir = "../ShapeDatabase_INFOMR")

mesh = vedo.Mesh(objFile)
plotter = vedo.Plotter(offscreen=True)
plotter.add(mesh)
plotter.show().screenshot('./temp_images/test.png')

# ~~
image = mpimg.imread('./temp_images/test.png')

nrows, ncols = 3, 5
figsize = [8, 8]

xs = np.linspace(0, 2*np.pi, 60)
ys = np.abs(np.sin(xs))

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

vedo_caller = VedoOpener()
btn_width = 0.065
bth_height = 0.025

btns = []

for i, axi in enumerate(ax.flat):
    rowid = i // ncols
    colid = i % ncols
    axi.axis('off')

    if rowid == 0 and colid == 2:
        axi.imshow(image)
        axi.set_title("base image", fontsize=16)
        axes = plt.axes([0.5 - (btn_width/2.0), 0.7 - (bth_height/2.0), btn_width, bth_height])
        btn_main = Button(axes, 'View')
        btn_main.on_clicked(vedo_caller.open)
    elif rowid > 0:
        axi.imshow(image)
        axi.set_title("return image " + str(i-5) + "\n$dist = 0.00$", fontsize=10)
        axes = plt.axes([0.5 - (btn_width/2.0) + (colid - float(ncols-1)/2.0)*0.195, 0.7 - (bth_height/2.0) - rowid * 0.32, btn_width, bth_height])
        btn = Button(axes, 'View')
        btns.append(btn)
        btns[i-5].on_clicked(vedo_caller.open)





plt.tight_layout()
plt.show()
# ~~

shutil.rmtree('./temp_images')





"""
TODOS:
- analyzer again: 50 bins
"""

