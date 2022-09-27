import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import scipy.io as sio

# load COIL20 dataset from matlab file
coil20 = sio.loadmat('COIL20.mat')
# extract data and labels
data = coil20['X']
labels = coil20['Y']

# perform PCA
pca = PCA(n_components=2)
pca.fit(data)
data_pca = pca.transform(data)

# plot the data
plt.figure()
plt.scatter(data_pca[:,0], data_pca[:,1], c=labels)
plt.show()