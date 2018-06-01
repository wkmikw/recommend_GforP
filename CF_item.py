#coding=utf-8
#__author__ = GaoY
#python CF_item.py

import numpy as np
import gc
import time
import math


def computing_M_relation(item1, item2, watched):
    p1 = watched[:, item1]
    p2 = watched[:, item2]
    count = 0
    for i in range(1, MAXUSER + 1):
        if p1[i] and p2[i]:
            count += 1
    sum1 = np.sum(p1)
    sum2 = np.sum(p2)
    return count/math.sqrt(sum1 * sum2) if sum1 and sum2 else 0


# 选出K个最大的
def MAX_K(ele, K):
    Max_list = np.zeros([K, 2]) # min in 0
    for index, val in enumerate(ele): # index:U_id, val:相似程度
        if val > Max_list[0][1]:
            Max_list[0] = [index, val]
            j = 1
            #重新有序化
            while j < K:
                if val > Max_list[j][1]:
                    Max_list[j-1] = Max_list[j]
                    Max_list[j] = index, val
                    j += 1
                else:
                    break
    return(Max_list)


def compute_interest_user(watched, user, popularity, M):
    Movie_interest = np.zeros(MAXMOVIE + 1)
    #是否看过
    label = watched[user]
    for i in range(MAXMOVIE + 1):
        if label[i]:
            Max_list = MAX_K(Movies_relationship[i], K)
            for ele in Max_list:
                Movie_interest[int(ele[0])] += ele[1] / math.log(10 + popularity[int(ele[0])])
    return(MAX_K(Movie_interest, M))

MAXMOVIE = 1682
MAXUSER = 943
K = 10 # 每部电影计算取的最相似电影数量
M = 10 # 推荐数量

train = np.load('data/train.npy')
popularity = np.load('data/popularity.npy')
# 观看记录矩阵
watched = np.zeros([MAXUSER + 1, MAXMOVIE + 1], dtype=int)
for ele in train:
    watched[ele[0]][ele[1]] = 1
np.save('data/watched', watched)

# computing similarity
# runtime=176s,可考虑进程并发
Movies_relationship = np.zeros([MAXMOVIE + 1, MAXMOVIE + 1])
start = time.time()
for i in range(1, MAXMOVIE + 1):
    for j in range(i + 1, MAXMOVIE + 1):
        Movies_relationship[i][j] = computing_M_relation(i , j, watched)
        Movies_relationship[j][i] = Movies_relationship[i][j]
    if i % 30 == 0:
        end = time.time()
        print('complete %d/1682 in %ds, remain %ds' % 
            (i, (end - start), ((end - start) / (i / MAXMOVIE) - (end - start))))
np.save('data/Movies_relationship', Movies_relationship)

# computing recommend list
recommend_list = np.zeros([MAXUSER + 1, M], dtype=int)
for i in range(1, MAXUSER + 1):
    temp = compute_interest_user(watched, i, popularity, M)
    temp = temp.T
    recommend_list[i] = temp[0]
np.save('data/recommend_list', recommend_list)


# test
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
print('Precision rate: %.2f%%' % (count / recommend_count * 100))
