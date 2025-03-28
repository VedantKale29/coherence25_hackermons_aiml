from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

print(cosine_similarity(arr1.reshape(1, -1), arr2.reshape(1, -1)))