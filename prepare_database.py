import sys

import pandas as pd

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
            f.write(row_to_string + "\n")

if __name__ == "__main__":
    # Load the data
    data = pd.read_csv(sys.argv[1])
    normalize_database(data)
    transform_data_for_knn(data)
