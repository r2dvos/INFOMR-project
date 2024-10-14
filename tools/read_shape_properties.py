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

    # Surface Area
    surface_area = df[df['File'].isin([obj_name])].iloc[0]['Area']
    print("Surface Area: " + str(surface_area))
    print("~~")

    # Compactness
    surface_area = df[df['File'].isin([obj_name])].iloc[0]['Compactness']
    print("Compactness: " + str(surface_area))
    print("~~")

    # 3D Regularity
    surface_area = df[df['File'].isin([obj_name])].iloc[0]['Regularity']
    print("3D Regularity: " + str(surface_area))
    print("~~")

    # Diameter
    surface_area = df[df['File'].isin([obj_name])].iloc[0]['Diameter']
    print("Diameter: " + str(surface_area))
    print("~~")

    # Convexity
    surface_area = df[df['File'].isin([obj_name])].iloc[0]['Convexity']
    print("SConvexity: " + str(surface_area))
    print("~~")

    # Eccentricity
    surface_area = df[df['File'].isin([obj_name])].iloc[0]['Eccentricity']
    print("Eccentricity: " + str(surface_area))
    print("~~")

    #A3
    print("A3: angle between 3 random vertices")
    print("~~")

    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['A3'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins A3'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("A3: angle between 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D1
    print("D1: distance between barycenter and random vertex")
    print("~~")

    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D1'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D1'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("D1: distance between barycenter and random vertex")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D2
    print("D2: distance between 2 random vertices")
    print("~~")

    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D2'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D2'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("D2: distance between 2 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D3
    print("D3: square root of area of triangle given by 3 random vertices")
    print("~~")

    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D3'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D3'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("D3: square root of area of triangle given by 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D4
    print("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    print("~~")

    hist = list(map(float, df[df['File'].isin([obj_name])].iloc[0]['D4'].replace('[', '').replace(']', '').split(', ')))
    bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['File'].isin([obj_name])].iloc[0]['Bins D4'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
    bin_centers = 0.5*(bins[1:]+bins[:-1])
    plt.plot(bin_centers,hist)
    plt.title("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

#
#~~~~~~~~~
#

def get_group_properties(input_csv: str, group_name: str) -> None:
    df = pd.read_csv(input_csv)

    #A3
    print("A3: angle between 3 random vertices")
    print("~~")

    for i in range(df['Class'].value_counts()[group_name]):
        hist = list(map(float, df[df['Class'].isin([group_name])].iloc[i]['A3'].replace('[', '').replace(']', '').split(', ')))
        bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['Class'].isin([group_name])].iloc[i]['Bins A3'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
        bin_centers = 0.5*(bins[1:]+bins[:-1])
        plt.plot(bin_centers,hist)
    plt.title("A3: angle between 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D1
    print("D1: distance between barycenter and random vertex")
    print("~~")
    for i in range(df['Class'].value_counts()[group_name]):
        hist = list(map(float, df[df['Class'].isin([group_name])].iloc[i]['D1'].replace('[', '').replace(']', '').split(', ')))
        bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['Class'].isin([group_name])].iloc[i]['Bins D1'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
        bin_centers = 0.5*(bins[1:]+bins[:-1])
        plt.plot(bin_centers,hist)
    plt.title("D1: distance between barycenter and random vertex")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D2
    print("D2: distance between 2 random vertices")
    print("~~")
    for i in range(df['Class'].value_counts()[group_name]):
        hist = list(map(float, df[df['Class'].isin([group_name])].iloc[i]['D2'].replace('[', '').replace(']', '').split(', ')))
        bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['Class'].isin([group_name])].iloc[i]['Bins D2'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
        bin_centers = 0.5*(bins[1:]+bins[:-1])
        plt.plot(bin_centers,hist)
    plt.title("D2: distance between 2 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D3
    print("D3: square root of area of triangle given by 3 random vertices")
    print("~~")
    for i in range(df['Class'].value_counts()[group_name]):
        hist = list(map(float, df[df['Class'].isin([group_name])].iloc[i]['D3'].replace('[', '').replace(']', '').split(', ')))
        bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['Class'].isin([group_name])].iloc[i]['Bins D3'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
        bin_centers = 0.5*(bins[1:]+bins[:-1])
        plt.plot(bin_centers,hist)
    plt.title("D3: square root of area of triangle given by 3 random vertices")
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

    #D4
    print("D4: cube root of volume of tetrahedron formed by 4 random vertices")
    print("~~")
    for i in range(df['Class'].value_counts()[group_name]):
        hist = list(map(float, df[df['Class'].isin([group_name])].iloc[i]['D4'].replace('[', '').replace(']', '').split(', ')))
        bins = np.array(list(map(float, list(filter(('').__ne__, re.sub(r'\s+', ' ', df[df['Class'].isin([group_name])].iloc[i]['Bins D4'].replace('[', '').replace(']', '').replace('\n', ' ')).split(' '))))))
        bin_centers = 0.5*(bins[1:]+bins[:-1])
        plt.plot(bin_centers,hist)
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
