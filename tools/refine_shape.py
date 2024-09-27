import pip
import numpy as np
if np.__version__==1.26:
    pass
else:
    pip.main(['install', 'numpy==1.26'])

import sys
import os
import tkinter as tk
from tkinter import filedialog
from manipulations import refine_mesh

TARGET: int = 5000
TARGET_RANGE: int = 500
DISTRIBUTION_SUBDIVISIONS: int = 3

def main(objFile: str, passes: int) -> None:
    refine_mesh(objFile, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    objFile = filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
    main(objFile, int(sys.argv[1]))
