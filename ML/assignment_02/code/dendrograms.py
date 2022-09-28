import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

AFFINITY = 'euclidean'
LINKAGES = ['single', 'complete', 'average', 'ward']

# Read data from csv file
data = pd.read_csv('data_clustering.csv', header=None)
data = data.values

for linkageMeasures in LINKAGES:
    # create hierarchical clustering model
    # generate and display dendrogram and color the clusters using the above set colors
    plt.figure(figsize=(10, 7))
    plt.title("Dendrogram for {} linkage".format(linkageMeasures))
    plt.xlabel("Data points")
    plt.ylabel("Euclidean distance")
    dendrogram(linkage(data, method=linkageMeasures,
               metric=AFFINITY), no_labels=True, color_threshold=0)

    # switch for linkage measures and the corresponding line
    if linkageMeasures == 'single':
        plt.axhline(y=0.153, color='r', linestyle='--')
        plt.text(0, 0.153 + 0.001, '2 clusters', color='r')
        plt.axhline(y=0.14, color='r', linestyle='--')
        plt.text(0, 0.14 + 0.001, '3 clusters', color='r')
        plt.axhline(y=0.12, color='r', linestyle='--')
        plt.text(0, 0.12 + 0.001, '4 clusters', color='r')
    elif linkageMeasures == 'complete':
        plt.axhline(y=0.72, color='r', linestyle='--')
        plt.text(0, 0.72 + 0.004, '2 clusters', color='r')
        plt.axhline(y=0.635, color='r', linestyle='--')
        plt.text(0, 0.635 + 0.004, '3 clusters', color='r')
        plt.axhline(y=0.55, color='r', linestyle='--')
        plt.text(0, 0.55 + 0.004, '4 clusters', color='r')
    elif linkageMeasures == 'average':
        plt.axhline(y=0.38, color='r', linestyle='--')
        plt.text(0, 0.38 + 0.003, '2 clusters', color='r')
        plt.axhline(y=0.2975, color='r', linestyle='--')
        plt.text(0, 0.2975 + 0.003, '3 clusters', color='r')
        plt.axhline(y=0.27, color='r', linestyle='--')
        plt.text(0, 0.27 + 0.003, '4 clusters', color='r')
    elif linkageMeasures == 'ward':
        plt.axhline(y=3.15, color='r', linestyle='--')
        plt.text(0, 3.15 + 0.02, '2 clusters', color='r')
        plt.axhline(y=2, color='r', linestyle='--')
        plt.text(0, 2 + 0.02, '3 clusters', color='r')
        plt.axhline(y=1.1, color='r', linestyle='--')
        plt.text(0, 1.1 + 0.02, '4 clusters', color='r')
    # save the dendrogram
    plt.savefig('output/dendrogram_{}.png'.format(linkageMeasures))
