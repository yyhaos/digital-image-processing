# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:39:48 2019

@author: Administrator
"""

import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
"""
PSF:point spread function 点扩散函数，参数 模糊方向 模糊尺度
逆滤波恢复法步骤：
    1.对退化图像g(x,y)作傅里叶变换G(u,v)
    2.计算系统点扩散函数h(x,y)的二维傅里叶变换H(u,v)
    3.逆滤波计算F(u,v) = G(u,v)/H(u,v)
    4.计算F(u,v)逆傅里叶变换,f(x,y)

"""

#运动模糊模板
def motion_psf(image_size, motion_angle, motion_num): #模糊角度，运动像素点个数
    PSF = np.zeros(image_size)  # 点扩散函数
    x_cen = (image_size[0] - 1) / 2 # 中心点
    y_cen = (image_size[1] - 1) / 2
 
    sin = math.sin(motion_angle * math.pi / 180)
    cos = math.cos(motion_angle * math.pi / 180)
 
    # 将对应角度上motion_num个点置成1
    for i in range(motion_num):
        x_offset = round(sin * i) # 保留至最近整数(保留0位小数)，同取偶
        y_offset = round(cos * i)
        PSF[int(x_cen - x_offset), int(y_cen + y_offset)] = 1
 
    return PSF 

#对图片进行运动模糊
def motion_blur(image, PSF, eps): 
    original_fft = np.fft.fft2(image) # 原图像傅里叶变换
    PSF_fft = np.fft.fft2(PSF) + eps  # 运动模糊
    blurred = np.fft.ifft2(original_fft * PSF_fft) # 傅里叶逆变换
    blurred = np.abs(np.fft.fftshift(blurred)) # 中心化
    return blurred

#逆滤波    
def inverse(blurred, PSF, eps):       
    blurred_fft = np.fft.fft2(blurred) # 退化图像傅里叶变换
    PSF_fft = np.fft.fft2(PSF) + eps  # 点扩散函数傅里叶变换
    result = np.fft.ifft2(blurred_fft / PSF_fft) # F(u,v)的傅里叶逆变换
    result = np.abs(np.fft.fftshift(result)) # 中心化
    return result

eps = 2e-3 #平均噪声功率，逆滤波时可能出现0
image = cv2.imread('lena.bmp')
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #转换为灰度图

PSF = motion_psf(image.shape, 45, 50) #设置运动方向和运动像素点个数
blurred = np.abs(motion_blur(image, PSF, eps)) #运动模糊
result = inverse(blurred, PSF, eps)   #逆滤波


plt.imshow(image,'gray')     #显示原图像
plt.title('original image')
plt.axis('off')
plt.show()


plt.imshow(blurred,'gray')   #显示运动模糊图像
plt.title('blurred image')
plt.axis('off')
plt.show()


plt.imshow(result,'gray')    #显示复原图像
plt.title('restored image')
plt.axis('off')
plt.show()

