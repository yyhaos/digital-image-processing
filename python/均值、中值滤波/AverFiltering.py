#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 18:11:04 2019

@author: 201611210213
均值滤波的范围为3*3
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np

#均值滤波3*3
def ave(img,i,j,c):
    #由于像素ubyte范围在0~255,超出范围会报错，为了避免像素加减运算溢出异常，将像素转化为整形进行计算
    x = int(img[i-1,j-1][c])+int(img[i-1,j][c])+int(img[i-1,j+1][c])\
    +int(img[i,j-1][c])+int(img[i,j][c])+int(img[i,j+1][c])\
    +int(img[i+1,j-1][c])+int(img[i+1,j][c])+int(img[i+1,j+1][c])
    x = x/9
    if x>255:
        x = 255
    return x
#均值滤波5*5
def ave2(img,i,j,c):
    #由于像素ubyte范围在0~255,超出范围会报错，为了避免像素加减运算溢出异常，将像素转化为整形进行计算
    x = int(img[i-2,j-2][c])+int(img[i-2,j-1][c])+int(img[i-2,j][c])\
    +int(img[i-2,j+1][c])+int(img[i-2,j+2][c])\
    +int(img[i-1,j-2][c])+int(img[i-1,j-1][c])+int(img[i-1,j][c])\
    +int(img[i-1,j+1][c])+int(img[i-1,j+2][c])\
    +int(img[i,j-2][c])+int(img[i,j-1][c])+int(img[i,j][c])\
    +int(img[i,j+1][c])+int(img[i,j+2][c])\
    +int(img[i+1,j-2][c])+int(img[i+1,j-1][c])+int(img[i+1,j][c])\
    +int(img[i+1,j+1][c])+int(img[i+1,j+2][c])\
    +int(img[i+2,j-2][c])+int(img[i+2,j-1][c])+int(img[i+2,j][c])\
    +int(img[i+2,j+1][c])+int(img[i+2,j+2][c])
    x = x/25
    if x>255:
        x = 255
    return x
#中值滤波3*3
def mid(img,i,j,c):
    x = []
    x.append(int(img[i-1,j-1][c]))
    x.append(int(img[i-1,j][c]))
    x.append(int(img[i-1,j+1][c]))
    x.append(int(img[i,j-1][c]))
    x.append(int(img[i,j][c]))
    x.append(int(img[i,j+1][c]))
    x.append(int(img[i+1,j-1][c]))
    x.append(int(img[i+1,j][c]))
    x.append(int(img[i+1,j+1][c]))
    median = np.median(x)
    if median>255:
        median = 255
    return median
#中值滤波5*5
def mid2(img,i,j,c):
    x = []
    x.append(int(img[i-2,j-2][c]))
    x.append(int(img[i-2,j-1][c]))
    x.append(int(img[i-2,j][c]))
    x.append(int(img[i-2,j+1][c]))
    x.append(int(img[i-2,j+2][c]))
    x.append(int(img[i-1,j-2][c]))
    x.append(int(img[i-1,j-1][c]))
    x.append(int(img[i-1,j][c]))
    x.append(int(img[i-1,j+1][c]))
    x.append(int(img[i-1,j++2][c]))
    x.append(int(img[i,j+2][c]))
    x.append(int(img[i,j+1][c]))
    x.append(int(img[i,j][c]))
    x.append(int(img[i,j-1][c]))
    x.append(int(img[i,j-2][c]))
    x.append(int(img[i+1,j-2][c]))
    x.append(int(img[i+1,j-1][c]))
    x.append(int(img[i+1,j][c]))
    x.append(int(img[i+1,j+1][c]))
    x.append(int(img[i+1,j+2][c]))
    x.append(int(img[i+2,j-2][c]))
    x.append(int(img[i+2,j-1][c]))
    x.append(int(img[i+2,j][c]))
    x.append(int(img[i+2,j+1][c]))
    x.append(int(img[i+2,j+2][c]))
    median = np.median(x)
    if median>255:
        median = 255
    return median

if __name__ =='__main__':
    #图像输入
    #filename = input("Please intput filename:")
    #img=cv2.imread(filename)
    img=cv2.imread("src.bmp")
    rows,cols,channels=img.shape
    dst=img.copy()
    dst2=img.copy()
    dst3=img.copy()
    dst4=img.copy()
    #均值滤波3*3
    for c in range(channels):
        for i in range(rows):
            for j in range(cols):
                if (i-1)>=0 and (j-1)>=0 and (i+1)<rows and (j+1)<cols:#边缘不处理
                    dst[i,j][c]=ave(img,i,j,c)
                    
    #中值滤波3*3
    for c in range(channels):
        for i in range(rows):
            for j in range(cols):
                if (i-1)>=0 and (j-1)>=0 and (i+1)<rows and (j+1)<cols:#边缘不处理
                    dst2[i,j][c]=mid(img,i,j,c)
    #均值滤波5*5
    for c in range(channels):
        for i in range(rows):
            for j in range(cols):
                if (i-2)>=0 and (j-2)>=0 and (i+2)<rows and (j+2)<cols:#边缘不处理
                    dst3[i,j][c]=ave2(img,i,j,c)
                    
    #中值滤波5*5
    for c in range(channels):
        for i in range(rows):
            for j in range(cols):
                if (i-2)>=0 and (j-2)>=0 and (i+2)<rows and (j+2)<cols:#边缘不处理
                    dst4[i,j][c]=mid2(img,i,j,c)
    #python已有函数
    dst5=cv2.blur(img,(5,5))       #均值滤波
    dst6 = cv2.medianBlur(img,5)   #中值滤波
    font = cv2.FONT_HERSHEY_SIMPLEX
                     
    #展示  
    plt.figure('adjust_gamma',figsize=(10,10))
    plt.subplot(3,3,1)
    plt.title('origin suga image')
    plt.imshow(img)
    plt.axis('off')
    
    plt.subplot(3,3,2)
    plt.title('my average filter 3*3')
    plt.imshow(dst)
    plt.axis('off')
    
    plt.subplot(3,3,3)
    plt.title('my median filter 3*3')
    plt.imshow(dst2)
    plt.axis('off')
    
    plt.subplot(3,3,4)
    plt.title('my average filter 5*5')
    plt.imshow(dst3)
    plt.axis('off')
    
    plt.subplot(3,3,5)
    plt.title('my median filter 5*5')
    plt.imshow(dst4)
    plt.axis('off')
    
    plt.subplot(3,3,7)
    plt.title('python average filter 5*5')
    plt.imshow(dst5)
    plt.axis('off')
    
    plt.subplot(3,3,8)
    plt.title('python median filter 5*5')
    plt.imshow(dst6)
    plt.axis('off')
    plt.show()
    #保存文件
    #cv2.imwrite("dst_ave.bmp", dst)
    #cv2.imwrite("dst_mid.bmp", dst2)
    #newname = input("Please intput filename:")
    #cv2.imwrite(newname, dst)