#coding=utf-8
#__author__ = GaoY
#python test.py

import numpy as np
import gc
import time
import math

MAXMOVIE = 1682
MAXUSER = 943
K = 5 # 每部电影计算取的最相似电影数量
M = 10 # 推荐数量

test = np.load('data/test.npy')
# initialize real_watch matrix
real_watch = np.zeros([MAXUSER + 1, MAXMOVIE + 1], dtype=int)
for ele in test:
    real_watch[ele[0]][ele[1]] = 1
recommend = np.zeros([MAXUSER + 1, MAXMOVIE + 1], dtype=int)
recommend_list = np.load('data/recommend_list.npy')
# initialize recommend matrix
for i in range(1, MAXUSER + 1):
    for j in recommend_list[i]:
        recommend[i, j] = 1
# recall rate
real_count = np.sum(real_watch)
count = 0
for i in range(1, MAXUSER + 1):
    for j in range(1, MAXMOVIE + 1):
        if real_watch[i, j] and recommend[i, j]:
            count += 1
print('Recall rate: %.2f%%' % (count / real_count * 100))

#precision rate
recommend_count = np.sum(recommend)
print('Recall rate: %.2f%%' % (count / recommend_count * 100))


'''
a = np.arange(16).reshape((4,4))

rec = np.load('data/recommend_list.npy')

print('complete %d/1682 in %ds, remain %ds' % 
            (i, (end - start), ((end - start) / (i / MAXMOVIE) - (end - start))))

'''