import sys

import pandas as pd
import numpy as np

def normalize_database(data: pd.DataFrame):
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
                row_to_string += f" {np.format_float_positional(A3[i], trim='-')}"
            for i in range(0, len(D1)):
                row_to_string += f" {np.format_float_positional(D1[i], trim='-')}"
            for i in range(0, len(D2)):
                row_to_string += f" {np.format_float_positional(D2[i], trim='-')}"
            for i in range(0, len(D3)):
                row_to_string += f" {np.format_float_positional(D3[i], trim='-')}"
            for i in range(0, len(D4)):
                row_to_string += f" {np.format_float_positional(D4[i], trim='-')}"
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
