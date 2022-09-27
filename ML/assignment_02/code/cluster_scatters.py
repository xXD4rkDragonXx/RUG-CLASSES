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


def calculateWSS(data, labels):
    # Calculate the WSS for the given data and labels

    # calculate the centroids
    centroids = np.zeros((len(np.unique(labels)), len(data[0])))
    for i in range(len(np.unique(labels))):
        centroids[i] = np.mean(data[labels == i], axis=0)

    # calculate the cluster sum of squares
    wss = 0
    for i in range(len(data)):
        wss += np.sum((data[i] - centroids[labels[i]]) ** 2)

    return wss


def calculateBSS(data, labels):
    # Calculate the BSS for the given data and labels

    # calculate the centroids
    centroids = np.zeros((len(np.unique(labels)), len(data[0])))
    for i in range(len(np.unique(labels))):
        centroids[i] = np.mean(data[labels == i], axis=0)

    # calculate the cluster sum of squares
    bss = 0
    for i in range(len(centroids)):
        bss += np.sum((centroids[i] - np.mean(centroids)) ** 2)

    return bss


for linkageMeasure in LINKAGES:
    for nClusters in range(MINCLUSTERS, MAXCLUSTERS + 1):
        hac = AgglomerativeClustering(
            n_clusters=nClusters, affinity=AFFINITY, linkage=linkageMeasure)
        # fit the model
        hac.fit(data)
        # display clusters in scatter plot
        plt.figure(figsize=(10, 7))
        plt.title("Scatter plot for {} linkage and {} clusters".format(
            linkageMeasure, nClusters))
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.scatter(data[:, 0], data[:, 1], c=hac.labels_, cmap='rainbow')
        print("{} WSS: {} with {} clusters".format(linkageMeasure,
              round(calculateWSS(data, hac.labels_), 2), nClusters))
        print("{} BSS: {} with {} clusters".format(linkageMeasure,
              round(calculateBSS(data, hac.labels_), 2), nClusters))

        # save the plot
        plt.savefig(
            'output/{}_{}_clusters.png'.format(linkageMeasure, nClusters))
