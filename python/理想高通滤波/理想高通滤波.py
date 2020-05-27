# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 20:49:57 2019

@author: Administrator
"""
import cv2
import numpy as np 
from matplotlib import pyplot as plt
"""
#理想高通滤波 HighPassFilter
使高频通过而使低频衰减
步骤：
1.读取图像
2.设置滤波半径
3.傅里叶变换并中心化
4.确定傅里叶变换的原点
5.设置滤波器
6.滤波 矩阵点乘
7.傅里叶逆变换
8.显示图像

#函数说明
fft.fft2 快速傅里叶变换
fft.ifft2 傅里叶逆变换
fft.fftshift 将fft输出中的直流分量移到频谱中央
fft.ifftshift 上述函数的逆操作

"""

img=cv2.imread('lena.bmp',0) #读取图像
rows,cols=img.shape
cen_row,cen_col=int(rows/2),int(cols/2) #确定傅里叶变换原点

filter1=np.ones((rows,cols),np.uint8) #设置滤波半径
filter2=np.ones((rows,cols),np.uint8)

filter1[cen_row-20:cen_row+20,cen_col-20:cen_col+20]=0 #将靠近频谱中心的部分低通信息设置为0-即高通滤波
filter2[cen_row-10:cen_row+10,cen_col-10:cen_col+10]=0

plt.subplot(121), plt.imshow(filter1, 'gray'), plt.title('filter1') #滤波器显示
#plt.axis('off')
plt.subplot(122), plt.imshow(filter2, 'gray'), plt.title('filter2') 
plt.show()


f=np.fft.fft2(img) #傅里叶变换
fshift=np.fft.fftshift(f) #中心化：将FFT输出中的直流分量移动到频谱的中央 
fimg = np.log(np.abs(fshift)) #fft结果是复数, 其绝对值结果是振幅
plt.subplot(121), plt.imshow(img, 'gray'), plt.title('Original') #频谱展示
plt.subplot(122), plt.imshow(fimg, 'gray'), plt.title('Fourier') 
plt.show()

fshift_1=fshift*filter1 #滤波
fshift_2=fshift*filter2

fimg_1 = np.log(np.abs(fshift_1)) #fft结果是复数, 其绝对值结果是振幅
fimg_2 = np.log(np.abs(fshift_2))
plt.subplot(121), plt.imshow(fimg_1, 'gray'), plt.title('after hpfilter1') #频谱展示
plt.subplot(122), plt.imshow(fimg_2, 'gray'), plt.title('after hpfilter2') 
plt.show()

f_ishift_1=np.fft.ifftshift(fshift_1) #逆中心化
f_ishift_2=np.fft.ifftshift(fshift_2)

img_back_1=np.fft.ifft2(f_ishift_1) #傅里叶逆变换
img_back_2=np.fft.ifft2(f_ishift_2)

img_back_1=np.abs(img_back_1) #复数转换 
img_back_2=np.abs(img_back_2)

plt.figure(figsize=(10,10)) #显示高通滤波图像
plt.subplot(221),plt.imshow(img,cmap='gray'),plt.title('original image')
plt.subplot(222),plt.imshow(img_back_1,cmap='gray'),plt.title('hpfilter image r=20')
plt.subplot(223),plt.imshow(img_back_2,cmap='gray'),plt.title('hpfilter image r=10')