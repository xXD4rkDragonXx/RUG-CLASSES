import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score


def dbscan(data, eps, min_pts):
    # Initialize all points as unvisited
    clusters = []
    noise = []
    visited = [False] * len(data)
    # For each unvisited point i
    for i in range(len(data)):
        if not visited[i]:
            visited[i] = True
            neighbors = regionQuery(data, i, eps)
            if len(neighbors) < min_pts:
                noise.append(i)
            else:
                expandCluster(data, i, neighbors, clusters, eps, min_pts, visited)
    # calculate silhouette score
    labels = np.zeros(len(data))
    for i in range(len(clusters)):
        for j in clusters[i]:
            labels[j] = i
    silhouetteScore = silhouette_score(data, labels)
    return clusters, noise, silhouetteScore


def expandCluster(data, i, neighbors, clusters, eps, min_pts, visited):
    # Create a new cluster set
    cluster = set([i])
    # For each point j in neighbors
    for j in neighbors:
        if not visited[j]:
            visited[j] = True
            neighbors2 = regionQuery(data, j, eps)
            if len(neighbors2) >= min_pts:
                neighbors += neighbors2
        cluster.add(j)
    clusters.append(cluster)


def regionQuery(data, i, eps):
    # Return all points within eps distance of point
    neighbors = []
    for j in range(len(data)):
        if distance(data[i], data[j]) <= eps:
            neighbors.append(j)
    return neighbors


def distance(p1, p2):
    # Euclidean distance
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def plotClusters(data, eps, k):
    """
    Plot the clusters and noise points.
    Also returns the silhouette score.
    """
    # run dbscan
    clusters, noise, silhouetteScore = dbscan(data, eps, k)

    # create len(clusters) colors for plotting using rainbow color map
    colors = plt.cm.rainbow(np.linspace(0, 1, len(clusters)))

    # plot clusters and noise where each cluster is a different color and noise is black
    plt.figure()
    for i in range(len(clusters)):
        cluster = clusters[i]
        for j in cluster:
            plt.scatter(data[j][0], data[j][1], color=colors[i % len(colors)])
    for i in noise:
        plt.scatter(data[i][0], data[i][1], color='k')
    plt.title('DBSCAN Clustering with eps = ' + str(eps) + ' and k = ' + str(k))
    # save plot to file
    plt.savefig('output/dbscan_eps_' + str(eps) + '_k_' + str(k) + '.png')
    # return silhouette score
    return silhouetteScore


def elbowPlotKNearestNeighbors(data, k, highligted_point):
    # Calculate the distance between each point and its k nearest neighbors
    nbrs = NearestNeighbors(n_neighbors=k).fit(data)
    distances, indices = nbrs.kneighbors(data)
    # sort the distances
    distances = np.sort(distances, axis=0)
    # plot the distances
    plt.figure()
    plt.plot(distances[:, k - 1])
    # get maximum distance for formatting plot
    max_distance = distances[:, k - 1].max()
    # highlight point and show its coordinates under the point
    plt.plot(highligted_point, distances[highligted_point, k - 1], 'ro')
    plt.annotate(
        '(eps: {:.4f})'.format(distances[highligted_point, k - 1]),
        xy=(highligted_point,
        distances[highligted_point, k - 1]),
        xytext=(highligted_point,
        distances[highligted_point, k - 1] - max_distance * 0.05))
    plt.xlabel('Points')
    plt.ylabel('Distance')
    plt.title('Elbow Plot for K = ' + str(k))
    # save plot to file
    plt.savefig('output/elbow_plot_k_' + str(k) + '.png')

def showSilhouetteScores(scoreObjects):
    # show table of silhouette scores
    plt.figure()
    plt.axis('off')
    plt.table(cellText=[
                    [scoreObject['k'], scoreObject['eps'], scoreObject['score']] for scoreObject in scoreObjects
                ],
                colLabels=['k', 'eps', 'silhouette score'],
                loc='center')
    plt.savefig('output/silhouette_scores.png')


# import data_clustering.csv
data = pd.read_csv('data_clustering.csv', header=None).values.tolist()

# create dictionary to store silhouette scores
silhouetteScores = [{'k': 0, 'eps': 0, 'score': 0} for _ in range(3)]
# create elbow plots for k = 3, 4, 5 to find best eps per k
# the best eps value is the point where the curvature of the plot is the most pronounced
elbowPlotKNearestNeighbors(data, 3, 172)
silhouetteScores[0]['k'] = 3
silhouetteScores[0]['eps'] = 0.0493
silhouetteScores[0]['score'] = plotClusters(data, 0.0493, 3)
elbowPlotKNearestNeighbors(data, 4, 184)
silhouetteScores[1]['k'] = 4
silhouetteScores[1]['eps'] = 0.071
silhouetteScores[1]['score'] = plotClusters(data, 0.071, 4)
elbowPlotKNearestNeighbors(data, 5, 180)
silhouetteScores[2]['k'] = 5
silhouetteScores[2]['eps'] = 0.0748
silhouetteScores[2]['score'] = plotClusters(data, 0.0748, 5)

# show table of silhouette scores
showSilhouetteScores(silhouetteScores)

plt.show()
