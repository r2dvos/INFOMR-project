import numpy as np
import tkinter as tk
import pandas as pd
import trimesh
import os
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
    distance = np.linalg.norm([A3_dist, D1_dist, D2_dist, D3_dist, D4_dist, area_dist, compactness_dist, regularity_dist, diameter_dist, convexity_dist, eccencitry_dist])   
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

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    path = tk.filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
    full_refine(path, 1, True)
    obj = trimesh.load_mesh(path)
    obj = normalize_shape(obj)
    properties = shape_properties(obj, path)[0]
    properties_list = list(properties)
    properties_list.insert(0, "padding")
    properties_list.insert(0, "padding")
    properties = tuple(properties_list)
    df = pd.read_csv("database.csv")
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
        entry = (df.iloc[i]['Class'], df.iloc[i]['File'], distance_between_features(my_obj, df.iloc[i]))
        distances.append(entry)
        print(f"Tested {i}")
    distances = np.array(distances, dtype=[('Class', 'U20'), ('File', 'U10'), ('Distance', float)])
    distances = np.sort(distances, order='Distance')
    print("Sorting...")
    for i in range(20):
        print(distances[i])

    os.remove(path)
    os.rename(path + '.bak', path)