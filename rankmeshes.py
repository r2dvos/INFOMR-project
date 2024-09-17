import os
import matplotlib.pyplot as plt
import numpy as np

initialdir = "../ShapeDatabase_INFOMR"

min_num = 0
min_obj = ""

max_num = 0
max_obj = ""

vert_obj = []

for root, dirs, files in os.walk(initialdir):
    for dir in dirs:
        for obj in os.listdir(os.path.join(root, dir)):
            if obj.endswith('.obj'):
                with open(initialdir + "/" + dir + "/" + obj) as f:
                    lines = f.readlines()

                vertices = len([line for line in lines if line.startswith('v ')])
                #faces = len([line for line in lines if line.startswith('f ')])

                print("vertices in " + obj + ": " + str(vertices))

                if min_num == 0 and max_num == 0:
                    min_num = vertices
                    min_obj = dir + "/" + obj

                    max_num = vertices
                    max_obj = dir + "/" + obj

                if vertices < min_num:
                    min_num = vertices
                    min_obj = dir + "/" + obj

                if vertices > max_num:
                    max_num = vertices
                    max_obj = dir + "/" + obj

                vert_obj.append(vertices)

print("Min vertices: " + min_obj + " with " + str(min_num) + " vertices.")
print("Max vertices: " + max_obj + " with " + str(max_num) + " vertices.")

plt.hist(vert_obj, bins=500)
plt.show()
