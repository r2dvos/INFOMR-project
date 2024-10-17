import numpy as np
import tkinter as tk
import pandas as pd

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
    A3_dist = earth_movers_distance(np.fromstring(features1['A3'][1:-1], sep=' '), np.fromstring(features2['A3'][1:-1], sep=' '))
    D1_dist = earth_movers_distance(np.fromstring(features1['D1'][1:-1], sep=' '), np.fromstring(features2['D1'][1:-1], sep=' '))
    D2_dist = earth_movers_distance(np.fromstring(features1['D2'][1:-1], sep=' '), np.fromstring(features2['D2'][1:-1], sep=' '))
    D3_dist = earth_movers_distance(np.fromstring(features1['D3'][1:-1], sep=' '), np.fromstring(features2['D3'][1:-1], sep=' '))
    D4_dist = earth_movers_distance(np.fromstring(features1['D4'][1:-1], sep=' '), np.fromstring(features2['D4'][1:-1], sep=' '))
    area_dist = features1['Area'] - features2['Area']
    compactness_dist = features1['Compactness'] - features2['Compactness']
    regularity_dist = features1['Regularity'] - features2['Regularity']
    diameter_dist = features1['Diameter'] - features2['Diameter']
    convexity_dist = features1['Convexity'] - features2['Convexity']
    eccencitry_dist = features1['Eccentricity'] - features2['Eccentricity']
    distance = np.linalg.norm([A3_dist, D1_dist, D2_dist, D3_dist, D4_dist, area_dist, compactness_dist, regularity_dist, diameter_dist, convexity_dist, eccencitry_dist])   
    return distance

if __name__ == "__main__":
    #root = tk.Tk()
    #root.withdraw()

    #objFile = tk.filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
    df = pd.read_csv("database.csv")
    print(df.columns)
    my_obj = df.iloc[0]
    for i in range(1, len(df)):
        print(distance_between_features(my_obj, df.iloc[i]))