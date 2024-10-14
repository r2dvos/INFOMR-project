import numpy as np

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import re

import numpy as np

def get_shape_class(file_path: str) -> str:
    return os.path.basename(os.path.dirname(file_path))

#
#~~~~~~~~~
#

def get_shape_properties(input_csv: str, obj_name: str) -> None:
    df = pd.read_csv(input_csv)

    #A3
    print("A3: angle between 3 random vertices")
    print("~~\n")
    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['A3'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins A3'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("A3: angle between 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D1
    print("D1: distance between barycenter and random vertex")
    print("~~\n")
    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D1'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D1'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("D1: distance between barycenter and random vertex")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D2
    print("D2: distance between 2 random vertices")
    print("~~\n")
    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D2'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D2'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("D2: distance between 2 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D3
    print("D3: square root of area of triangle given by 3 random vertices")
    print("~~\n")
    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D3'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D3'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("D3: square root of area of triangle given by 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D4
    print("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    print("~~\n")
    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D4'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D4'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
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
                n, x = np.histogram(df['A3'].dropna(), bins=500)
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
                n, x = np.histogram(df['D1'].dropna(), bins=200)
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
                n, x = np.histogram(df['D2'].dropna(), bins=500)
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
                n, x = np.histogram(df['D3'].dropna(), bins=500)
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
                n, x = np.histogram(df['D4'].dropna(), bins=500)
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
    help = "Usage:\n-s: View shape properties of a single shape. Args: data csv, object name\n-g: View shape properties of a category. Args: data csv, category name.\n-h: Display this help message"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print(help)
        sys.exit()

    if mode == "-s" and len(sys.argv) == 4:
        get_shape_properties(sys.argv[2], sys.argv[3])
    elif mode == "-g" and len(sys.argv) == 4:
        get_group_properties(sys.argv[2], sys.argv[3])
    else:
        print(help)
