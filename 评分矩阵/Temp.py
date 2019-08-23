import numpy as np
List = np.array([[0, 1, 2, 3, 4, 2, 3, 2, 43, 5, 2], [0, 1, 2, 3, 4, 2, 3, 2, 43, 5, 2]])
print(List == 2)
print(np.where(List == 2))

print(type(np.zeros((5, 6), dtype=int)))

print([[2, 3, 4], [3, 4, 5]][1][2])
