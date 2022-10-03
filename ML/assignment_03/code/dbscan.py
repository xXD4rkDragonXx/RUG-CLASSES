import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def dbscan(data, eps, min_pts):
    # Initialize all points as unvisited
    clusters = []
    noise = []
    visited = [False] * len(data)
    # For each unvisited point i
    for i in range(len(data)):
        if not visited[i]:
            visited[i] = True
            neighbors = region_query(data, i, eps)
            if len(neighbors) < min_pts:
                noise.append(i)
            else:
                expand_cluster(data, i, neighbors, clusters, eps, min_pts, visited)
    return clusters, noise


def expand_cluster(data, i, neighbors, clusters, eps, min_pts, visited):
    # Create a new cluster set
    cluster = set([i])
    # For each point j in neighbors
    for j in neighbors:
        if not visited[j]:
            visited[j] = True
            neighbors2 = region_query(data, j, eps)
            if len(neighbors2) >= min_pts:
                neighbors += neighbors2
        cluster.add(j)
    clusters.append(cluster)


def region_query(data, i, eps):
    # Return all points within eps distance of point
    neighbors = []
    for j in range(len(data)):
        if distance(data[i], data[j]) <= eps:
            neighbors.append(j)
    return neighbors


def distance(p1, p2):
    # Euclidean distance
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# import data_clustering.csv
data = pd.read_csv('data_clustering.csv', header=None).values.tolist()

# run dbscan
clusters, noise = dbscan(data, 0.07, 3)
print('Amount of clusters:', len(clusters))

# create len(clusters) colors for plotting using rainbow color map
colors = plt.cm.rainbow(np.linspace(0, 1, len(clusters)))

# find common points between clusters and noise
common = []
for cluster in clusters:
    for i in noise:
        if i in cluster:
            common.append(i)

# if this is not empty, Some error has occurred.
# A point can not be both in a cluster and in noise or another cluster
print('Common points:', common)

# plot clusters and noise where each cluster is a different color and noise is black
for i in range(len(clusters)):
    cluster = clusters[i]
    print("Cluster {}: {}".format(i, cluster))
    for j in cluster:
        plt.scatter(data[j][0], data[j][1], color=colors[i % len(colors)])
for i in noise:
    plt.scatter(data[i][0], data[i][1], color='k')
print("amount of points: ", len(noise) + sum([len(cluster) for cluster in clusters]))
plt.show()
