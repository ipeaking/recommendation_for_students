import matplotlib.pyplot as plt
# import numpy as np
import math


def decay_function(alpha=0.01, init=1000, deltaT=100):  # decay衰变
    data = []
    for t in range(deltaT):
        if len(data) == 0:
            temp = init /math.pow(t+1, alpha)#math.exp(-alpha * math.log(t + 1))    math.pow(x, y)是说x的y次方
        else:
            temp = data[-1]/math.pow(t+1, alpha)# * math.exp(-alpha * math.log(t + 1))
        data.append(temp)

    plt.plot([t for t in range(deltaT)], data, label='alpha={}'.format(alpha)) # 画x, y, 标题


init = 10000
deltaT = 60
plt.figure(figsize=(20, 8)) # 画布

decay_function(0.005, init, deltaT)

plt.xticks([t for t in range(deltaT)]) # plt.xticks()表达的是x轴的刻度内容的范围
plt.grid()  # 生成网格
plt.legend() # 将样例显示出来
plt.show() # 生成图片