# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 18:43:04 2019

@author: Nancy
"""
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

#读入图片
img=cv2.imread('1.jpg',0)
#np.fft.fft2()函数实现傅里叶变换
#np.fft.fftshift()函数来实现平移,让直流分量在输出图像的重心 
dft = np.fft.fft2(img)
dtf_shift=np.fft.fftshift(dft) 
ori = np.log(np.abs(dtf_shift))
plt.imshow(ori, 'gray'),plt.title('pinpuori') #显示之前的频谱
plt.show()

r,c=img.shape 
new=np.zeros((r,c),np.uint8) 
def lixiang(radius):
    dist1=radius  #设置半径
    for i in range (r):
        for j in range (c): 
            if(math.sqrt((i-r/2)*(i-r/2)+(j-c/2)*(j-c/2)) <= dist1):
                new[i,j]=1 
    filter1 = np.abs(new)
    plt.imshow(filter1, 'gray'),plt.title('filter') #显示滤波器频谱
    plt.show()
    fshift=dtf_shift*new
    return fshift

#傅立叶逆变换
result1 = lixiang(30)
later = np.log(np.abs(result1))
plt.imshow(later, 'gray'),plt.title('pinpulat')  #显示之后频谱
plt.show()
f_ishift=np.fft.ifftshift(result1) 
img2 = np.fft.ifft2(f_ishift) 
img2=np.abs(img2)
img2=(img2-np.amin(2))/(np.amax(img2)-np.amin(img2))


plt.figure(figsize=(15,15))
plt.subplot(121),plt.imshow(img,cmap='gray'),plt.title('input image')
plt.subplot(122),plt.imshow(img2,cmap='gray'),plt.title('output image')

