import sys

import pandas as pd
import numpy as np

def normalize_database(data: pd.DataFrame):
    print(f"Area mean: {data['Area'].mean()} std: {data['Area'].std()}")
    print(f"Compactness mean: {data['Compactness'].mean()} std: {data['Compactness'].std()}")
    print(f"Regularity mean: {data['Regularity'].mean()} std: {data['Regularity'].std()}")
    print(f"Diameter mean: {data['Diameter'].mean()} std: {data['Diameter'].std()}")
    print(f"Convexity mean: {data['Convexity'].mean()} std: {data['Convexity'].std()}")
    print(f"Eccentricity mean: {data['Eccentricity'].mean()} std: {data['Eccentricity'].std()}")

    # Normalize the data
    data['Area'] = (data['Area'] - data['Area'].mean()) / data['Area'].std()
    data['Compactness'] = (data['Compactness'] - data['Compactness'].mean()) / data['Compactness'].std()
    data['Regularity'] = (data['Regularity'] - data['Regularity'].mean()) / data['Regularity'].std()
    data['Diameter'] = (data['Diameter'] - data['Diameter'].mean()) / data['Diameter'].std()
    data['Convexity'] = (data['Convexity'] - data['Convexity'].mean()) / data['Convexity'].std()
    data['Eccentricity'] = (data['Eccentricity'] - data['Eccentricity'].mean()) / data['Eccentricity'].std()

    data.to_csv("database.csv", index=False)

def transform_data_for_knn(data: pd.DataFrame):
    with open("knn_data.txt", "w") as f:
        for i in range(0, len(data)):
            current_row = data.iloc[i]
            row_to_string = f"{current_row['Area']} {current_row['Compactness']} {current_row['Regularity']} {current_row['Diameter']} {current_row['Convexity']} {current_row['Eccentricity']}"
            A3 = current_row['A3']
            D1 = current_row['D1']
            D2 = current_row['D2']
            D3 = current_row['D3']
            D4 = current_row['D4']
            for i in range(0, len(A3)):
                row_to_string += f" {A3[i]}"
            for i in range(0, len(D1)):
                row_to_string += f" {D1[i]}"
            for i in range(0, len(D2)):
                row_to_string += f" {D2[i]}"
            for i in range(0, len(D3)):
                row_to_string += f" {D3[i]}"
            for i in range(0, len(D4)):
                row_to_string += f" {D4[i]}"
            f.write(row_to_string + "\n")

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv(sys.argv[1])

    normalize_database(df)
    for i in range(0, len(df)):
        df.at[i, 'A3'] = np.fromstring(df.at[i, 'A3'][1:-1], sep=', ')
        df.at[i, 'D1'] = np.fromstring(df.at[i, 'D1'][1:-1], sep=', ')
        df.at[i, 'D2'] = np.fromstring(df.at[i, 'D2'][1:-1], sep=', ')
        df.at[i, 'D3'] = np.fromstring(df.at[i, 'D3'][1:-1], sep=', ')
        df.at[i, 'D4'] = np.fromstring(df.at[i, 'D4'][1:-1], sep=', ')
    transform_data_for_knn(df)
