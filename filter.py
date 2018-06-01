#coding=utf-8
#__author__ = GaoY

#python filter.py

import numpy as np
import gc
import time
import math
import random

MAXMOVIE = 1682
MAXUSER = 943

def SplitData(data, M, k, seed):
    test = []
    train = []
    random.seed(seed)
    for ele in data:
        if random.randint(0, M) == k:
            test.append([ele[0], ele[1]])
        else:
            train.append([ele[0], ele[1]])
    return test, train
if __name__ == '__main__':
    data = np.loadtxt('data/data.csv', dtype=int, delimiter=',')
    test, train = SplitData(data, 88, 5, 1)
    test = np.array(test)
    train = np.array(train)

    gc.collect()
    np.save('data/test', test)
    np.save('data/train', train)






