import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

AFFINITY = 'euclidean'
MINCLUSTERS = 2
MAXCLUSTERS = 4


def ownSilhouetteScore(data, labels):
    # Calculate the silhouette score for the given data and labels

    # Calculate intra-cluster distances
    intraClusterDistances = np.zeros(len(data))
    for i in range(len(data)):
        # Calculate the average distance to all other points in the same cluster
        intraClusterDistances[i] = np.mean(np.linalg.norm(
            data[labels == labels[i]] - data[i], axis=1))

    # Calculate inter-cluster distances
    interClusterDistances = np.zeros(len(data))
    for i in range(len(data)):
        # Calculate the average distance to all other points in the nearest cluster
        interClusterDistances[i] = np.min(
            np.mean(np.linalg.norm(data[labels != labels[i]] - data[i], axis=1)))

    # Calculate the silhouette score
    silhouetteScore = np.mean((interClusterDistances - intraClusterDistances) /
                              np.maximum(intraClusterDistances, interClusterDistances))

    return silhouetteScore


# Read data from csv file
data = pd.read_csv('data_clustering.csv', header=None)
data = data.values

# calculate silhouette score for different configuations of the model
results = {'single': [], 'complete': [], 'average': [], 'ward': []}
nclustersList = range(MINCLUSTERS, MAXCLUSTERS + 1)
for nClusters in nclustersList:
    for linkage in results.keys():
        hac = AgglomerativeClustering(
            n_clusters=nClusters, affinity=AFFINITY, linkage=linkage)
        hac.fit(data)
        results[linkage].append(silhouette_score(data, hac.labels_, ))

# display results in a bar chart
x = np.arange(len(nclustersList))
width = 0.20
fig, ax = plt.subplots()
plt.ylim(top=1)
rects1 = ax.bar(x - 2*width, results['single'], width, label='Single')
rects2 = ax.bar(x - width, results['complete'], width, label='Complete')
rects3 = ax.bar(x, results['average'], width, label='Average')
rects4 = ax.bar(x + width, results['ward'], width, label='Ward')
for rect in rects1 + rects2 + rects3 + rects4:
    height = rect.get_height()
    ax.annotate(round(height, 2),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                textcoords="offset points",
                ha='center', va='bottom', rotation=22.5)
ax.set_ylabel('Silhouette score')
ax.set_xlabel('Number of clusters')
ax.set_title('Silhouette score for different configurations')
ax.set_xticks(x)
ax.set_xticklabels(nclustersList)
ax.legend()
fig.tight_layout()
plt.show()
