import sys

import pandas as pd

if __name__ == "__main__":
    # Load the data
    data = pd.read_csv(sys.argv[1])

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

    data.to_csv("normalized_data.csv", index=False)