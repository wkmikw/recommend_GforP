#coding=utf-8
#__author__ = GaoY
#python CF_item.py

import numpy as np
import gc
import time
import math
from multiprocessing import Pool, Process, Queue

from filter import SplitData
from err_logging import log

def computing_popularity(train):
    #train = np.load('data/train.npy')
    popularity = np.zeros(MAXMOVIE + 1, dtype=int)
    for i in train:
        popularity[i[1]] += 1
    np.save('data/popularity', popularity)
    return popularity

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

def compute_interest_user(watched, user, popularity, M, Movies_relationship):
    Movie_interest = np.zeros(MAXMOVIE + 1)
    #是否看过
    label = watched[user]
    for i in range(MAXMOVIE + 1):
        if label[i]:
            Max_list = MAX_K(Movies_relationship[i], K)
            for ele in Max_list:
                if watched[user,int(ele[0])]:
                    continue
                Movie_interest[int(ele[0])] += ele[1] / math.log(10 + popularity[int(ele[0])])

    return(MAX_K(Movie_interest, M))

def Generate_watched(train):
    # 观看记录矩阵
    watched = np.zeros([MAXUSER + 1, MAXMOVIE + 1], dtype=int)
    for ele in train:
        watched[ele[0]][ele[1]] = 1
    #np.save('data/watched', watched)
    return watched

# computing similarity
@log
def Computing_similarity(watched):
    Movies_relationship = np.zeros([MAXMOVIE + 1, MAXMOVIE + 1])
    start = time.time()
    for i in range(1, MAXMOVIE + 1):
        for j in range(i + 1, MAXMOVIE + 1):
            Movies_relationship[i][j] = computing_M_relation(i , j, watched)
            Movies_relationship[j][i] = Movies_relationship[i][j]
        if i % 500 == 0:
            end = time.time()
            #print('complete %d/1682 in %ds, remain %ds' % 
            #    (i, (end - start), ((end - start) / (i / MAXMOVIE) - (end - start))))
            #print('complete %d/1682 in %ds, remain %ds' % 
            #    (i, (end - start), ((end - start) / ((2*MAXMOVIE-i)*i/MAXMOVIE**2) - (end - start))))
    #np.save('data/Movies_relationship', Movies_relationship)
    return Movies_relationship

# computing recommend list
@log
def Computing_recommend_list(watched, popularity, Movies_relationship):
    recommend_list = np.zeros([MAXUSER + 1, M], dtype=int)
    for i in range(1, MAXUSER + 1):
        temp = compute_interest_user(watched, i, popularity, M, Movies_relationship)
        temp = temp.T
        recommend_list[i] = temp[0]
    #np.save('data/recommend_list', recommend_list)
    return recommend_list


# test
# initialize real_watch matrix
@log
def Test(watched, recommend_list, test):
    real_watch = np.zeros([MAXUSER + 1, MAXMOVIE + 1], dtype=int)
    for ele in test:
        real_watch[ele[0]][ele[1]] = 1
    recommend = np.zeros([MAXUSER + 1, MAXMOVIE + 1], dtype=int)
    #recommend_list = np.load('data/recommend_list.npy')
    # initialize recommend matrix
    for i in range(1, MAXUSER + 1):
        for j in recommend_list[i]:
            recommend[i, j] = 1

    #测试是否筛掉了已看过的
    count = 0
    for i in range(1, MAXUSER + 1):
        for j in range(1, MAXMOVIE + 1):
            if watched[i, j] and recommend[i, j]:
                count += 1
    print(count)

    # recall rate
    real_count = np.sum(real_watch)
    count = 0
    for i in range(1, MAXUSER + 1):
        for j in range(1, MAXMOVIE + 1):
            if real_watch[i, j] and recommend[i, j]:
                count += 1
    
    Recall_rate = count / real_count * 100
    print('Recall rate: %.2f%%' % (count / real_count * 100))
    #precision rate
    recommend_count = np.sum(recommend)
    Precision_rate = count / recommend_count * 100
    print('Precision rate: %.2f%%' % (count / recommend_count * 100))
    return Recall_rate, Precision_rate

# main cycle
def Main_cycle(k, q):
    start = time.time()
    test, train = SplitData(Step, k, 1)
    watched = Generate_watched(train)
    popularity = computing_popularity(train)
    Movies_relationship = Computing_similarity(watched)
    recommend_list = Computing_recommend_list(watched, popularity, Movies_relationship)
    Recall_rate, Precision_rate = Test(watched, recommend_list, test)
    q.put([Recall_rate, Precision_rate])
    end = time.time()
    print('Task %d completed in %ds' % (k, (end - start)))

if __name__ == '__main__':
    
    MAXMOVIE = 1682
    MAXUSER = 943
    K = 10 # 每部电影计算取的最相似电影数量
    M = 20 # 推荐数量
    Step = 11

    q = Queue()
    for k in range(3):
        a = []
        for i in range(4):
            if i+k*4 < 11:
                p =  Process(target=Main_cycle, args=(i+k*4, q,))
                a.append(p)
        for p in a:
            p.start()
        for p in a:
            p.join()
    Recall_rate = 0
    Precision_rate = 0
    i = 0
    while i < 11:
        value = q.get(True)
        Recall_rate += value[0]
        Precision_rate += value[1]
        i += 1
    print('Recall rate: %.2f%%' % (Recall_rate / 11))
    print('Precision_rate: %.2f%%' % (Precision_rate / 11))
    print('All subprocesses done.')