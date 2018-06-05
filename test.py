#coding=utf-8
#__author__ = GaoY
#python test.py



import numpy as np
import gc
import time
import math

def Hash_Q_item(data):
    DIVISION1 = 1000
    DIVISION2 = 1000000 
    Hash_Q = np.zeros((NUM_ITEMS + 1, 3))
    temp1st = data[0, 1] // DIVISION1
    temp2nd = data[0, 1] // DIVISION2
    #temp3rd = 1
    cur1st = 1
    cur2nd = 1
    cur3rd = 1
    for i in range(data.shape[0]):
        code = data[i, 1]
        if code // DIVISION1 == temp1st: # 同一二级知识点
            Hash_Q[i] = [cur1st, cur2nd, cur3rd]
        else if code // DIVISION2 == temp2nd: # 同一一级知识点
            cur1st += 1
            temp1st = code // DIVISION1
            Hash_Q[i] = [cur1st, cur2nd, cur3rd]
        else: # 不同的一级知识点
            cur1st += 1
            cur2nd += 1
            temp1st = code // DIVISION1
            temp2nd = code // DIVISION2
            Hash_Q[i] = [cur1st, cur2nd, cur3rd]
    return Hash_Q

data = np.loadtxt('data/date.csv', dtype=int, delimiter=',')
Hash_Q = Hash_Q_item(data)
print(Hash_Q)

'''

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



a = np.arange(16).reshape((4,4))

rec = np.load('data/recommend_list.npy')

print('complete %d/1682 in %ds, remain %ds' % 
            (i, (end - start), ((end - start) / (i / MAXMOVIE) - (end - start))))



for i in popularity:
    if i == 0:
        print('e')




from multiprocessing import Pool, Process
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    
    a = []
    for i in range(3):
        p =  Process(target=long_time_task, args=(i,))
        a.append(p)
    for p in a:
        p.start()
    for p in a:
        p.join()
    print('All subprocesses done.')



data = np.loadtxt('data/date.csv', dtype=int, delimiter=',')

'''