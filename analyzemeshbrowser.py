from vedo import load
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

objFile = filedialog.askopenfilename(initialdir = "../ShapeDatabase_INFOMR")

shape = load(objFile)
num_vertices = len(shape.vertices)
num_faces = len(shape.cells)

face_types = set(len(face) for face in shape.cells)
if face_types == {3}:
    face_type = "Only triangles"
elif face_types == {4}:
    face_type = "Only quads"
else:
    face_type = "Mixed triangles and quads"

bounding_box = shape.bounds()

print("Shape Analyzed: Vertices - ", num_vertices, ", Faces - ", num_faces, ", Face Types - ", face_type, ", Bounding Box - ", bounding_box)
