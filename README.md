# INFOMR-project

**How to run**

The databases are already included in the repository, so you can skip to the querying section.

## Preprocessing

    ./refine.py
    ./normalization.py

Both programs have a help option, which can be accessed by running the program with the `-h` flag.

## Feature extraction

    ./gather_shape_properties.py

This will create a database file in the selected database directory. It contains non-normalized shape properties.

    ./prepare_database.py

Creates a normalized database file in the current directory and a database for the KNN.

Both programs have a help option, which can be accessed by running the program with the `-h` flag.

## Querying

    ./query.py --normal

or

    ./query.py --knn

A pop-up window will appear, where you can select the query file. The shape will be refined and normalized, and the properties will be gathered. The program will then search for the most similar 10 shapes in the database and display it.