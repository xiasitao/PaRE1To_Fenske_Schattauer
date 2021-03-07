This directory hosts all clustering and cluster analysis logic and results.

In clusters all resulting clusters, also selected quality benchmarks are saved.
In financial_statement, the distance matrices for the fin stat-based clustering are created.
In hp, the Hoberg Phillips clusters are stored.
In medoids, the medoids and their respective cluster memebers for n = 10, 20, 30 are stored.
In plots, all plots are stored.
In sp500, the distance matrices for the stock returns-based clustering are created.

cluster_analysis.ipynb takes the computed clusters and creates quality measures, medoid files and plots.
distance_matrix_analysis.ipynb takes the distance matrices and clusters the companies.
