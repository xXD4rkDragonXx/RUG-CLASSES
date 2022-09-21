# execute PCA using calculations instead of importing on the COIL20 dataset and plot the results.

import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

# load COIL20 dataset from matlab file
coil20 = sio.loadmat('COIL20.mat')
# extract data and labels
data = coil20['X']
labels = coil20['Y']

# perform PCA
# calculate the mean of each column
mean = np.mean(data, axis=0)
# subtract the mean from each column
data = data - mean
# calculate the covariance matrix
cov = np.cov(data, rowvar=False)
# calculate the eigenvalues and eigenvectors of the covariance matrix
eigval, eigvec = np.linalg.eig(cov)
# sort the eigenvalues and eigenvectors in descending order
idx = eigval.argsort()[::-1]
eigval = eigval[idx]
eigvec = eigvec[:,idx]
# select the first two eigenvectors
eigvec = eigvec[:,0:2]
# project the data onto the eigenvectors
data_pca = np.dot(data, eigvec)

# eigen-value profile of the data set
# plt.figure()
# plt.plot(eigval)
# plt.show()

# table reporting the dimensionality d if we want to keep 0.9, 0.95 and 0.98 fraction of the total variance
print('d\t0.9\t0.95\t0.98')
d90, d95, d98 = 0, 0, 0
for i in range(1, len(eigval)):
    variance = np.sum(eigval[0:i])/np.sum(eigval)
    if variance >= 0.9 and d90 == 0:
        d90 = i
    if variance >= 0.95 and d95 == 0:
        d95 = i
    if variance >= 0.98 and d98 == 0:
        d98 = i
print('%d\t%d\t%d\t%d' % (len(eigval), d90, d95, d98))

# print a plot showing the reduced data using t-SNE calculated using numpy


# plot the data
# plt.figure()
# plt.scatter(data_pca[:,0], data_pca[:,1], c=labels)
# plt.show()
