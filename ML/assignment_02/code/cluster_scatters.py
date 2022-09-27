import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

AFFINITY = 'euclidean'
LINKAGES = ['single', 'complete', 'average', 'ward']
MINCLUSTERS = 2
MAXCLUSTERS = 4

# Read data from csv file
data = pd.read_csv('data_clustering.csv', header=None)
data = data.values

# display data in scatter plot
plt.figure(figsize=(10, 7))
plt.title("Data without clustering")
plt.scatter(data[:, 0], data[:, 1], c='black', s=7)
plt.savefig('output/data_scatter.png')

for linkageMeasures in LINKAGES:
    for nClusters in range(MINCLUSTERS, MAXCLUSTERS + 1):
        hac = AgglomerativeClustering(
            n_clusters=nClusters, affinity=AFFINITY, linkage=linkageMeasures)
        # fit the model
        hac.fit(data)
        # display clusters in scatter plot
        plt.figure(figsize=(10, 7))
        plt.title("Scatter plot for {} linkage and {} clusters".format(
            linkageMeasures, nClusters))
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.scatter(data[:, 0], data[:, 1], c=hac.labels_, cmap='rainbow')
        # save the plot
        plt.savefig('output/{}_{}_clusters.png'.format(linkageMeasures, nClusters))
