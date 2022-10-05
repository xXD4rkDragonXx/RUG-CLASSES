import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# Load data
mat = scipy.io.loadmat("thyroid.mat")

# Extract data
X = mat['X']
y = mat['y']

# Standardize data
X = StandardScaler().fit_transform(X)

def k_nearest_neighbors(X, k_array):
    eps = 0
    for k in k_array:
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(X)
        distances, indices = nbrs.kneighbors(X)
        distances = np.sort(distances, axis=0)
        if distances[:, k - 1].max() > eps:
            eps = distances[:, k - 1].max()
    return eps

k_array = [10,11,12]

max_eps = k_nearest_neighbors(X, k_array)

# Compute DBSCAN
db = DBSCAN(eps=max_eps, min_samples=12).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True

falseNegatives = 0
falsePositives = 0
truePositives = 0
trueNegatives = 0
wrong = 0

for i in range(len(db.labels_)):
    if db.labels_[i] < 0:
        if y[i] == 1:
            falseNegatives += 1
            wrong += 1
            print("Wrongly classified as noise: ", i)
        else:
            trueNegatives += 1
    else:
        if y[i] == 0:
            truePositives += 1
        else:
            falsePositives += 1
            wrong += 1
            print("Wrongly classified as cluster: ", i)

precision = truePositives / (truePositives + falsePositives)
recall = truePositives / (truePositives + falseNegatives)
f_measure = 2 * (precision * recall) / (precision + recall)

print("Wrong: ", wrong)
print("Correct: ", len(db.labels_)-wrong)
print("True Positives: ", truePositives)
print("True Negatives: ", trueNegatives)
print("False Positives: ", falsePositives)
print("False Negatives: ", falseNegatives)
print("Precision: ", precision)
print("Recall: ", recall)
print("F_measure: ", f_measure)