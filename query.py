import vedo
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import trimesh
import os

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button
import numpy as np
import shutil

from gather_shape_properties import shape_properties
from normalization import normalize_shape
from refine import full_refine


def first_nonzero(dirt_or_holes: np.ndarray) -> int:
    dim = dirt_or_holes.size
    for i in range(dim):
        if dirt_or_holes[i] > 0.0:
            return i
    return -1

def move_dirt(dirt, from_idx, holes, to_idx) -> tuple[float, float, list[float], list[float]]:
    if dirt[from_idx] <= holes[to_idx]:
        flow = dirt[from_idx]
        dirt[from_idx] = 0.0
        holes[to_idx] -= flow
    elif dirt[from_idx] > holes[to_idx]:
        flow = holes[to_idx]
        dirt[from_idx] -= flow
        holes[to_idx] = 0.0
    dist = np.abs(from_idx - to_idx)
    return flow, dist, dirt, holes

def earth_movers_distance(dirt: np.ndarray, holes: np.ndarray) -> float:
    dirt_c = np.copy(dirt) 
    holes_c = np.copy(holes)
    tot_work = 0.0

    while True:  # todo: add sanity counter check
        from_idx = first_nonzero(dirt_c)
        to_idx = first_nonzero(holes_c)
        if from_idx == -1 or to_idx == -1:
            break
        (flow, dist, dirt_c, holes_c) = move_dirt(dirt_c, from_idx, holes_c, to_idx)
        tot_work += flow * dist
    return tot_work

def distance_between_features(features1: pd.Series, features2: pd.Series) -> float:
    A3_dist = earth_movers_distance(features1['A3'], features2['A3'])
    D1_dist = earth_movers_distance(features1['D1'], features2['D1'])
    D2_dist = earth_movers_distance(features1['D2'], features2['D2'])
    D3_dist = earth_movers_distance(features1['D3'], features2['D3'])
    D4_dist = earth_movers_distance(features1['D4'], features2['D4'])
    area_dist = features1['Area'] - features2['Area']
    compactness_dist = features1['Compactness'] - features2['Compactness']
    regularity_dist = features1['Regularity'] - features2['Regularity']
    diameter_dist = features1['Diameter'] - features2['Diameter']
    convexity_dist = features1['Convexity'] - features2['Convexity']
    eccencitry_dist = features1['Eccentricity'] - features2['Eccentricity']
    #distance = np.linalg.norm([A3_dist, D1_dist, D2_dist, D3_dist, D4_dist, area_dist, compactness_dist, regularity_dist, diameter_dist, convexity_dist, eccencitry_dist]) 
    distance = A3_dist + D1_dist + D2_dist + D3_dist + D4_dist + area_dist + compactness_dist + regularity_dist + diameter_dist + convexity_dist + eccencitry_dist  
    return distance

def distance_between_features2(features1: pd.Series, features2: pd.Series) -> float:
    features1_array = np.array([
        features1['Area'],
        features1['Compactness'],
        features1['Regularity'],
        features1['Diameter'],
        features1['Convexity'],
        features1['Eccentricity'],
        *np.fromstring(features1['A3'][1:-1], sep=', '),
        *np.fromstring(features1['D1'][1:-1], sep=', '),
        *np.fromstring(features1['D2'][1:-1], sep=', '),
        *np.fromstring(features1['D3'][1:-1], sep=', '),
        *np.fromstring(features1['D4'][1:-1], sep=', ')
        ])
    features2_array = np.array([
        features2['Area'],
        features2['Compactness'],
        features2['Regularity'],
        features2['Diameter'],
        features2['Convexity'],
        features2['Eccentricity'],
        *np.fromstring(features2['A3'][1:-1], sep=', '),
        *np.fromstring(features2['D1'][1:-1], sep=', '),
        *np.fromstring(features2['D2'][1:-1], sep=', '),
        *np.fromstring(features2['D3'][1:-1], sep=', '),
        *np.fromstring(features2['D4'][1:-1], sep=', ')
        ])
    distance = earth_movers_distance(features1_array, features2_array)
    return distance

def normalize_query(properties_list, df):
    properties_list[0] = (properties_list[0] - df["Area"].mean()) / df["Area"].std()
    properties_list[1] = (properties_list[1] - df["Compactness"].mean()) / df["Compactness"].std()
    properties_list[2] = (properties_list[2] - df["Regularity"].mean()) / df["Regularity"].std()
    properties_list[3] = (properties_list[3] - df["Diameter"].mean()) / df["Diameter"].std()
    properties_list[4] = (properties_list[4] - df["Convexity"].mean()) / df["Convexity"].std()
    properties_list[5] = (properties_list[5] - df["Eccentricity"].mean()) / df["Eccentricity"].std()
    return properties_list

###########################################################################################################################################################


def result_printer(queryObj, returnObjs, queryInfo, returnInfos, dists): 
    def btn_open(index):
        def clicked(event):
            mesh = vedo.Mesh(obj_shapes[index])
            vedo.show(mesh, axes=0)
            vedo.close()
        return clicked

    def btn_info(index):
        def clicked(event):
            print("~~")
            print(obj_infos[index])
        return clicked

    shutil.rmtree('./temp_images', ignore_errors=True)
    Path("./temp_images").mkdir(parents=True, exist_ok=True)

    root = tk.Tk()
    root.withdraw()

    mesh = vedo.Mesh(queryObj)
    plotter = vedo.Plotter(offscreen=True)
    plotter.add(mesh)
    plotter.show().screenshot('./temp_images/query.png')

    for i in range(10):
        mesh = vedo.Mesh(returnObjs[i])
        plotter = vedo.Plotter(offscreen=True)
        plotter.add(mesh)
        plotter.show().screenshot("./temp_images/return_" + str(i) + ".png")

    # /\/

    obj_shapes = []
    obj_infos = []

    obj_shapes.append(queryObj)
    obj_infos.append(queryInfo)
    for i in range(10):
        obj_shapes.append(returnObjs[i])
        obj_infos.append(returnInfos[i])

    # ~~
    nrows, ncols = 3, 5
    figsize = [8, 8]

    xs = np.linspace(0, 2*np.pi, 60)
    ys = np.abs(np.sin(xs))

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    btn_width = 0.065
    bth_height = 0.025

    btns_view = []
    btns_info = []

    for i, axi in enumerate(ax.flat):
        rowid = i // ncols
        colid = i % ncols
        axi.axis('off')

        if rowid == 0 and colid == 2:
            image = mpimg.imread('./temp_images/query.png')
            axi.imshow(image)
            axi.set_title("base image", fontsize=16)
            axes = plt.axes([0.5 - (btn_width/2.0), 0.7 - (bth_height/2.0), btn_width, bth_height])
            btn_view_main = Button(axes, 'View')
            btn_view_main.on_clicked(btn_open(index = 0))
            axes = plt.axes([0.5 - (btn_width/2.0), 0.665 - (bth_height/2.0), btn_width, bth_height])
            btn_info_main = Button(axes, 'Info')
            btn_info_main.on_clicked(btn_info(index = 0))
        elif rowid > 0:
            image = mpimg.imread("./temp_images/return_" + str(i-5) + ".png")
            axi.imshow(image)
            axi.set_title("return image " + str(i-4) + "\n$dist = $" + str(round(dists[i-5], 4)), fontsize=10)
            axes = plt.axes([0.5 - (btn_width/2.0) + (colid - float(ncols-1)/2.0)*0.195, 0.7 - (bth_height/2.0) - rowid * 0.32, btn_width, bth_height])
            btn = Button(axes, 'View')
            btns_view.append(btn)
            btns_view[i-5].on_clicked(btn_open(index = i-4))
            axes = plt.axes([0.5 - (btn_width/2.0) + (colid - float(ncols-1)/2.0)*0.195, 0.665 - (bth_height/2.0) - rowid * 0.32, btn_width, bth_height])
            btn = Button(axes, 'Info')
            btns_info.append(btn)
            btns_info[i-5].on_clicked(btn_info(index = i-4))




    plt.tight_layout()
    plt.show()
    # ~~

    shutil.rmtree('./temp_images')


###########################################################################################################################################################


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    path_to_db = "../ShapeDatabase_INFOMR"

    path = tk.filedialog.askopenfilename(initialdir = path_to_db)
    full_refine(path, 1, True)
    obj = trimesh.load_mesh(path)
    obj = normalize_shape(obj)
    df = pd.read_csv("database.csv")

    properties = shape_properties(obj, path)[0]
    properties_list = list(properties)
    print(properties_list)
    properties_list = normalize_query(properties_list, df)
    print(properties_list)
    """
    properties_list.insert(0, "padding")
    properties_list.insert(0, "padding")
    properties = tuple(properties_list)
    
    column_headers = df.columns
    my_obj = pd.Series(properties, index=column_headers)
    distances = []

    for i in range(0, len(df)):
        df.at[i, 'A3'] = np.fromstring(df.at[i, 'A3'][1:-1], sep=', ')
        df.at[i, 'D1'] = np.fromstring(df.at[i, 'D1'][1:-1], sep=', ')
        df.at[i, 'D2'] = np.fromstring(df.at[i, 'D2'][1:-1], sep=', ')
        df.at[i, 'D3'] = np.fromstring(df.at[i, 'D3'][1:-1], sep=', ')
        df.at[i, 'D4'] = np.fromstring(df.at[i, 'D4'][1:-1], sep=', ')

    for i in range(0, len(df)):
        entry = (df.iloc[i]['Class'], df.iloc[i]['File'], distance_between_features(my_obj, df.iloc[i]), df.iloc[i]['Area'], df.iloc[i]['Compactness'], df.iloc[i]['Regularity'], df.iloc[i]['Diameter'], df.iloc[i]['Convexity'], df.iloc[i]['Eccentricity'])
        distances.append(entry)
        print(f"Tested {i}")
    distances = np.array(distances, dtype=[('Class', 'U20'), ('File', 'U10'), ('Distance', float), ('Area', float), ('Compactness', float), ('Regularity', float), ('Diameter', float), ('Convexity', float), ('Eccentricity', float)])
    distances = np.sort(distances, order='Distance')
    distances_fancy = pd.DataFrame(data = distances)

    queryObj = path
    queryInfo = my_obj[['Area', 'Compactness', 'Regularity', 'Diameter', 'Convexity', 'Eccentricity']]

    returnObjs = []
    returnInfos = []
    dists = []
    for i in range(10):
        returnObjs.append(path_to_db + "/" + distances[i]['Class'] + "/" + distances[i]['File'])
        returnInfos.append(distances_fancy.iloc[i][['Class', 'File', 'Distance', 'Area', 'Compactness', 'Regularity', 'Diameter', 'Convexity', 'Eccentricity']])
        dists.append(distances[i][['Distance']].astype(float))

    result_printer(queryObj, returnObjs, queryInfo, returnInfos, dists)
    """
    os.remove(path)
    os.rename(path + '.bak', path)
