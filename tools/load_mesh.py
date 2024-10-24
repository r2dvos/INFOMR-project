import vedo
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

objFile = filedialog.askopenfilename(initialdir = "../ShapeDatabase_INFOMR")

mesh = vedo.Mesh(objFile)
vedo.show(mesh, axes=2)

# notes: resampling first, principal component analysis after, normalization later
# subdivide & decimate multiple times
# meshing uniformity
# histograms to show normalization worked well
