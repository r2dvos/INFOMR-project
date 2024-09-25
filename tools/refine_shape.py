import sys
import tkinter as tk
from tkinter import filedialog
from manipulations import refine_mesh
import trimesh

TARGET: int = 5000
TARGET_RANGE: int = 500

def main(objFile: str, passes: int) -> None:
    model = trimesh.load(objFile)
    print(f"Loaded {objFile}")
    refine_mesh(model, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    objFile = filedialog.askopenfilename(initialdir = "../ShapeDatabase_INFOMR_copy")
    main(objFile, int(sys.argv[1]))
