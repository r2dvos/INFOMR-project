import numpy as np

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from vedo import Mesh, load
import numpy as np
from shape_property_descriptors import A3, D1, D2, D3, D4

ANALYSIS_VALUES: int = 2000

def get_shape_class(file_path: str) -> str:
    return os.path.basename(os.path.dirname(file_path))

#
#~~~~~~~~~
#

def write_properties(db_path: str, output_path: str) -> None:
    for root, _, files in os.walk(db_path):
        for file in files:
            if file.endswith('.obj'):
                obj_path = os.path.join(root, file)
                shape_class = get_shape_class(obj_path)
                print("extracting properties of " + shape_class + "/" + file)

                shape: Mesh = load(obj_path)

                """
                data_A3 = []
                random_array_A3 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES * 3, replace=False)
                random_array_A3_0 = random_array_A3[0:ANALYSIS_VALUES]
                random_array_A3_1 = random_array_A3[ANALYSIS_VALUES + 1:ANALYSIS_VALUES * 2]
                random_array_A3_2 = random_array_A3[(ANALYSIS_VALUES * 2) + 1:ANALYSIS_VALUES * 3]
                data_D1 = []
                random_array_D1_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D2 = []
                random_array_D2 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES * 2, replace=False)
                random_array_D2_0 = random_array_D2[0:ANALYSIS_VALUES]
                random_array_D2_1 = random_array_D2[ANALYSIS_VALUES + 1:ANALYSIS_VALUES * 2]
                data_D3 = []
                random_array_D3 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES * 3, replace=False)
                random_array_D3_0 = random_array_D3[0:ANALYSIS_VALUES]
                random_array_D3_1 = random_array_D3[ANALYSIS_VALUES + 1:ANALYSIS_VALUES * 2]
                random_array_D3_2 = random_array_D3[(ANALYSIS_VALUES * 2) + 1:ANALYSIS_VALUES * 3]
                data_D4 = []
                random_array_D4 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES * 4, replace=False)
                random_array_D4_0 = random_array_D4[0:ANALYSIS_VALUES]
                random_array_D4_1 = random_array_D4[ANALYSIS_VALUES + 1:ANALYSIS_VALUES * 2]
                random_array_D4_2 = random_array_D4[(ANALYSIS_VALUES * 2) + 1:ANALYSIS_VALUES * 3]
                random_array_D4_2 = random_array_D4[(ANALYSIS_VALUES * 3) + 1:ANALYSIS_VALUES * 4]
                """

                data_A3 = []
                random_array_A3_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_A3_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_A3_2 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D1 = []
                random_array_D1_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D2 = []
                random_array_D2_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D2_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D3 = []
                random_array_D3_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D3_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D3_2 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D4 = []
                random_array_D4_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D4_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D4_2 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D4_3 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                for i in range(ANALYSIS_VALUES):
                    data_D1.append(D1(shape.vertices[random_array_D1_0[i]]))
                    if random_array_D2_0[i] != random_array_D2_1[i]:
                        data_D2.append(D2(shape.vertices[random_array_D2_0[i]], shape.vertices[random_array_D2_1[i]]))
                    if random_array_A3_0[i] != random_array_A3_1[i] and random_array_A3_0[i] != random_array_A3_2[i] and random_array_A3_1[i] != random_array_A3_2[i]:
                        data_A3.append(A3(shape.vertices[random_array_A3_0[i]], shape.vertices[random_array_A3_1[i]], shape.vertices[random_array_A3_2[i]]))
                    if random_array_D3_0[i] != random_array_D3_1[i] and random_array_D3_0[i] != random_array_D3_2[i] and random_array_D3_1[i] != random_array_D3_2[i]:
                        data_D3.append(D3(shape.vertices[random_array_D3_0[i]], shape.vertices[random_array_D3_1[i]], shape.vertices[random_array_D3_2[i]]))
                    if random_array_D4_0[i] != random_array_D4_1[i] and random_array_D4_0[i] != random_array_D4_2[i] and random_array_D4_0[i] != random_array_D4_3[i] and random_array_D4_1[i] != random_array_D4_2[i] and random_array_D4_1[i] != random_array_D4_3[i] and random_array_D4_2[i] != random_array_D4_3[i]:
                        data_D4.append(D4(shape.vertices[random_array_D4_0[i]], shape.vertices[random_array_D4_1[i]], shape.vertices[random_array_D4_2[i]], shape.vertices[random_array_D4_3[i]]))
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
