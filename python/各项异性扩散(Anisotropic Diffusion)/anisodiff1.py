from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math

lena = Image.open('lena.jpg').convert('L')
lena = np.array(lena)
m = lena.shape[0]
n = lena.shape[1]
kappa = 15  # 导热系数,控制平滑
lamb = 0.15  # 控制平滑
num_iter = 20  # 迭代次数
imgn = np.zeros((m, n))
for i in range(1, num_iter):#按迭代次数的循环
    for p in range(2, m - 1):#按图像第二维长度循环
        for q in range(2, n - 1):#按图像第一维长度循环
            #对四个方向上的当前像素求偏导
            NI = lena[p - 1][q] - lena[p][q]
            SI = lena[p + 1][q] - lena[p][q]
            EI = lena[p][q - 1] - lena[p][q]
            WI = lena[p][q + 1] - lena[p][q]

            # 计算导热系数
            cN = math.exp(-(NI ** 2) / (kappa * kappa))
            cS = math.exp(-(SI ** 2) / (kappa * kappa))
            cE = math.exp(-(EI ** 2) / (kappa * kappa))
            cW = math.exp(-(WI ** 2) / (kappa * kappa))
            imgn[p][q] = lena[p][q] + lamb * (cN * NI + cS * SI + cE * EI + cW * WI)  # 扩散后的新值
    lena = imgn
lena = Image.fromarray(lena)
#显示图像
plt.figure('lena')
plt.imshow(lena)
plt.show()