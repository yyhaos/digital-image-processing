#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 18:19:04 2019

@author: macos
"""

import numpy
import cv2 as cv
import matplotlib.pyplot as plt
 
def FFT_v1(Img,Wr):
    if Img.shape[0]==2:
        pic = numpy.zeros([2],dtype=complex)
        pic = pic*(1+0j)
        pic[0]=Img[0]+Img[1]*Wr[0]
        pic[1]=Img[0]-Img[1]*Wr[0]
        return pic
    else:
        pic = numpy.empty([Img.shape[0]],dtype=complex)
        pic[0:Img.shape[0]//2] = FFT_v1(Img[::2],Wr[::2])+Wr*FFT_v1(Img[1::2],Wr[::2])
        pic[Img.shape[0]//2:Img.shape[0]]=FFT_v1(Img[::2],Wr[::2])-Wr*FFT_v1(Img[1::2],Wr[::2])
        return pic;
 
 
def FFT_1d(Img):
    #计算旋转因子
    Wr = numpy.ones([Img.shape[0]//2])*[numpy.cos(2*numpy.pi*i/Img.shape[0])-1j*numpy.sin(2*numpy.pi*i/Img.shape[0]) for i in numpy.arange(Img.shape[0]/2)]
    return FFT_v1(Img,Wr)
 
 
def FFT_2d(Img):
    pic = numpy.zeros([Img.shape[0],Img.shape[1]],dtype=complex)
    #对行进行FFT
    for i in numpy.arange(Img.shape[0]):
        pic[:,i]=FFT_1d(Img[:,i])
    #对列进行FFT
    for i in numpy.arange(Img.shape[1]):
        pic[i,:]=FFT_1d(pic[i,:])
    return pic
#略bug
#def FFTshift(f,raws,cols):
#    fshift = numpy.zeros([raws,cols],dtype=complex)
#    fshift[0:raws//2, 0:cols//2] = f[raws//2:raws, cols//2:cols]
#    fshift[0:raws//2, cols//2:cols] = f[raws//2:raws, 0:cols//2]
#    fshift[raws//2:raws, 0:cols//2] = f[0:raws//2:raws, cols//2:cols]
#    fshift[raws//2:raws, cols//2:cols] = f[0:raws//2, 0:cols//2]
#    return fshift

if __name__ =='__main__':
    #读取图像并转换为灰度图
    img = cv.imread('lena.png')
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    r,l = gray.shape
    #自写程序：
    f = FFT_2d(gray)
    #fshift = FFTshift(f,r,l) 
    fshift = numpy.fft.fftshift(f)
    fimg = numpy.log(numpy.abs(fshift))
    
    #利用内置函数
    ff = numpy.fft.fft2(gray) # 快速傅里叶变换算法得到频率分布  
    ffshift = numpy.fft.fftshift(ff) # 默认结果中心点位置是在左上角，转移到中间位置
    ffimg = numpy.log(numpy.abs(ffshift)) # fft 结果是复数，求绝对值结果才是振幅
     
  
    plt.subplot(131), plt.imshow(img, 'gray'), plt.title('Original')  
    plt.subplot(132), plt.imshow(fimg, 'gray'), plt.title('fft')  
    plt.subplot(133), plt.imshow(ffimg, 'gray'), plt.title('np.fft')  
    plt.show()
    
    print((abs(f - ff) < 0.0000001).all())