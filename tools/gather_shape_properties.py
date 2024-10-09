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
                total_value_A3 = 0
                greatest_value_A3 = 0
                random_array_A3_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_A3_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_A3_2 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D1 = []
                total_value_D1 = 0
                greatest_value_D1 = 0
                random_array_D1_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D2 = []
                total_value_D2 = 0
                greatest_value_D2 = 0
                random_array_D2_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D2_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D3 = []
                total_value_D3 = 0
                greatest_value_D3 = 0
                random_array_D3_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D3_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D3_2 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                data_D4 = []
                total_value_D4 = 0
                greatest_value_D4 = 0
                random_array_D4_0 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D4_1 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D4_2 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)
                random_array_D4_3 = np.random.choice(range(len(shape.vertices)), ANALYSIS_VALUES, replace=False)

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Part 1: calculations
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                for i in range(ANALYSIS_VALUES):
                    D1_val = D1(shape.vertices[random_array_D1_0[i]])
                    data_D1.append(D1_val)
                    total_value_D1 = total_value_D1 + D1_val
                    if D1_val > greatest_value_D1:
                        greatest_value_D1 = D1_val
                    if random_array_D2_0[i] != random_array_D2_1[i]:
                        D2_val = D2(shape.vertices[random_array_D2_0[i]], shape.vertices[random_array_D2_1[i]])
                        data_D2.append(D2_val)
                        total_value_D2 = total_value_D2 + D2_val
                        if D2_val > greatest_value_D2:
                            greatest_value_D2 = D2_val
                    if random_array_A3_0[i] != random_array_A3_1[i] and random_array_A3_0[i] != random_array_A3_2[i] and random_array_A3_1[i] != random_array_A3_2[i]:
                        A3_val = A3(shape.vertices[random_array_A3_0[i]], shape.vertices[random_array_A3_1[i]], shape.vertices[random_array_A3_2[i]])
                        data_A3.append(A3_val)
                        total_value_A3 = total_value_A3 + A3_val
                        if A3_val > greatest_value_A3:
                            greatest_value_A3 = A3_val
                    if random_array_D3_0[i] != random_array_D3_1[i] and random_array_D3_0[i] != random_array_D3_2[i] and random_array_D3_1[i] != random_array_D3_2[i]:
                        D3_val = D3(shape.vertices[random_array_D3_0[i]], shape.vertices[random_array_D3_1[i]], shape.vertices[random_array_D3_2[i]])
                        data_D3.append(D3_val)
                        total_value_D3 = total_value_D3 + D3_val
                        if D3_val > greatest_value_D3:
                            greatest_value_D3 = D3_val
                    if(random_array_D4_0[i] != random_array_D4_1[i] and random_array_D4_0[i] != random_array_D4_2[i] and random_array_D4_0[i] != random_array_D4_3[i] and
                       random_array_D4_1[i] != random_array_D4_2[i] and random_array_D4_1[i] != random_array_D4_3[i] and random_array_D4_2[i] != random_array_D4_3[i]):
                        D4_val = D4(shape.vertices[random_array_D4_0[i]], shape.vertices[random_array_D4_1[i]], shape.vertices[random_array_D4_2[i]], shape.vertices[random_array_D4_3[i]])
                        data_D4.append(D4_val)
                        total_value_D4 = total_value_D4 + D4_val
                        if D4_val > greatest_value_D4:
                            greatest_value_D4 = D4_val
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Part 2: normalizations 
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                for i in range(ANALYSIS_VALUES):
                    if i < len(data_D1):
                        data_D1[i] = data_D1[i]/greatest_value_D1
                    if i < len(data_D2):
                        data_D2[i] = data_D2[i]/greatest_value_D2
                    if i < len(data_A3):
                        data_A3[i] = data_A3[i]/greatest_value_A3
                    if i < len(data_D3):
                        data_D3[i] = data_D3[i]/greatest_value_D3
                    if i < len(data_D4):
                        data_D4[i] = data_D4[i]/greatest_value_D4
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

    #A3
    print("A3: angle between 3 random vertices")
    print("~~\n")

    n, x = np.histogram(df['A3'].dropna(), bins=100)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers,n)
    plt.title("A3: angle between 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D1
    print("D1: distance between barycenter and random vertex")
    print("~~\n")

    n, x = np.histogram(df['D1'].dropna(), bins=100)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers,n)
    plt.title("D1: distance between barycenter and random vertex")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D2
    print("D2: distance between 2 random vertices")
    print("~~\n")

    n, x = np.histogram(df['D2'].dropna(), bins=100)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers,n)
    plt.title("D2: distance between 2 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D3
    print("D3: square root of area of triangle given by 3 random vertices")
    print("~~\n")

    n, x = np.histogram(df['D3'].dropna(), bins=100)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers,n)
    plt.title("D3: square root of area of triangle given by 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D4
    print("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    print("~~\n")

    n, x = np.histogram(df['D4'].dropna(), bins=100)
    bin_centers = 0.5*(x[1:]+x[:-1])
    plt.plot(bin_centers,n)
    plt.title("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

#
#~~~~~~~~~
#

def get_group_properties(group_path: str) -> None:
    #A3
    print("A3: angle between 3 random vertices")
    print("~~\n")
    for root, _, files in os.walk(group_path):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                df = pd.read_csv(csv_path)
                n, x = np.histogram(df['A3'].dropna(), bins=100)
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n)

    plt.title("A3: angle between 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D1
    print("D1: distance between barycenter and random vertex")
    print("~~\n")
    for root, _, files in os.walk(group_path):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                df = pd.read_csv(csv_path)
                n, x = np.histogram(df['D1'].dropna(), bins=100)
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n)

    plt.title("D1: distance between barycenter and random vertex")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D2
    print("D2: distance between 2 random vertices")
    print("~~\n")
    for root, _, files in os.walk(group_path):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                df = pd.read_csv(csv_path)
                n, x = np.histogram(df['D2'].dropna(), bins=100)
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n)

    plt.title("D2: distance between 2 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D3
    print("D3: square root of area of triangle given by 3 random vertices")
    print("~~\n")
    for root, _, files in os.walk(group_path):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                df = pd.read_csv(csv_path)
                n, x = np.histogram(df['D3'].dropna(), bins=100)
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n)

    plt.title("D3: square root of area of triangle given by 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D4
    print("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    print("~~\n")
    for root, _, files in os.walk(group_path):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                df = pd.read_csv(csv_path)
                n, x = np.histogram(df['D4'].dropna(), bins=100)
                bin_centers = 0.5*(x[1:]+x[:-1])
                plt.plot(bin_centers,n)

    plt.title("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

#
#~~~~~~~~~
#

if __name__ == "__main__":
    help = "Usage:\n-d: Select a database to gather shape properties. Args: path to database, output folder\n-f: View shape properties of a single shape. Args: data csv\n-c: View shape properties of a category. Args: path to folder containing data csvs.\n-h: Display this help message"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print(help)
        sys.exit()

    if mode == "-f" and len(sys.argv) == 3:
        get_shape_properties(sys.argv[2])
    elif mode == "-c" and len(sys.argv) == 3:
        get_group_properties(sys.argv[2])
    elif mode == "-d" and len(sys.argv) == 4:
        write_properties(sys.argv[2], sys.argv[3])
    else:
        print(help)
