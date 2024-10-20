import os
import sys
from vedo import *
import tkinter as tk
from tkinter import filedialog

k = 3 # how many meshes we want to compare
root = tk.Tk()
root.withdraw()

plt = Plotter(shape=(1,k))
i = 0
while i < k:
    objFile = filedialog.askopenfilename(initialdir = "../ShapeDatabase_INFOMR")
    mesh = Mesh(objFile)
    plt.at(i).show(mesh, axes=2)
    i = i + 1

plt.interactive().close()