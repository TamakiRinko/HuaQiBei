import pandas as pd
from sklearn import preprocessing
import numpy as np
pathIndex = "../基金列表及属性/"

Frame = pd.read_csv(pathIndex + "基金属性.csv")
print(Frame)

