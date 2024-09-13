import vedo
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

objFile = filedialog.askopenfilename()

mesh = vedo.Mesh(objFile)
vedo.show(mesh)
