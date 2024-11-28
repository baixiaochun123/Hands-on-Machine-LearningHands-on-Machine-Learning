import random 
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class KMeans:
    """Kmeans聚类算法
    
    Parameters:
    ----------
    k:int
        聚类的数目.
        max_iter:int
        最大迭代次数.
        varepsilon:float
        判断是否收敛,如果两次迭代中心点距离小于varepsilon,则认为已经收敛.
        则说明算法已经收敛
    """
    def _init_(self,k=2,max_iterations= 500,varespsilion=0.0001):
        self.k = k
        self.max_iterations = max_iterations
        self.varepsilon = varespsilion
    
    #从所有样本中随机选取self.k个样本作为初始的聚类中心
    def init_random_centroids(self, X):
        n_samples, n_features = np.shape(X)
        centroids = np.zeros((self.k,n_features))
        for i in range(self.k):
            centroids[i] = data[np.random.choice(range(n_samples))]
        return centroids
    

    def _closest_centroid(self ,sample , centroids):
        distances = euclidean_distance(sample,centroids)
        closet
    
    def 
    