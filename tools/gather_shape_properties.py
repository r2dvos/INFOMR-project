import numpy as np

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from vedo import Mesh, load
import numpy as np
from shape_property_descriptors import A3, D1, D2, D3, D4

def get_shape_class(file_path: str) -> str:
    return os.path.basename(os.path.dirname(file_path))

#
#~~~~~~~~~
#

def write_properties(db_path: str, output_path: str) -> None:
    for root, _, files in os.walk(db_path):
        for file in files:
            if file.endswith('.obj'):
                print("extracting properties of " + file)
                obj_path = os.path.join(root, file)

                shape_class = get_shape_class(obj_path)
                shape: Mesh = load(obj_path)

                data_A3 = []
                data_D1 = []
                data_D2 = []
                data_D3 = []
                data_D4 = []

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                for i in range(len(shape.vertices)):
                    # Property D1
                    data_D1.append(D1(shape.vertices[i]))
                    for j in range(i+1, len(shape.vertices)):
                        # Property D2
                        data_D2.append(D2(shape.vertices[i], shape.vertices[j]))
                        for k in range(j+1, len(shape.vertices)):
                            # Properties A3, D3
                            data_A3.append(A3(shape.vertices[i], shape.vertices[j], shape.vertices[k]))
                            data_D3.append(D3(shape.vertices[i], shape.vertices[j], shape.vertices[k]))
                            for l in range(k+1, len(shape.vertices)):
                                # Property D4
                                data_D4.append(D4(shape.vertices[i], shape.vertices[j], shape.vertices[k], shape.vertices[l]))
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
                data_dict = dict(A3 = data_A3,
                                 D1 = data_D1,
                                 D2 = data_D2,
                                 D3 = data_D3,
                                 D4 = data_D4)

                Path(output_path + "/" + shape_class).mkdir(parents=True, exist_ok=True)
                df = pd.DataFrame(dict([(c, pd.Series(v)) for c, v in data_dict.items()]))
                output_csv = file.replace(".obj", ".csv")
                df.to_csv(output_path + "/" + shape_class + "/" + output_csv, index=False)
#
#~~~~~~~~~
#

def get_shape_properties(input_csv: str) -> None:
    df = pd.read_csv(input_csv)

#
#~~~~~~~~~
#

if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_shape_properties(sys.argv[1])
    elif len(sys.argv) > 2:
        write_properties(sys.argv[1], sys.argv[2])
    else:
        print("Please provide: \n 1 - a csv to read data from or \n 2 - a path to the database and an output folder")
