import numpy as np
import cv2
import math

def myErode(img,n,kernel):#腐蚀
    if n % 2 != 1:
        print('error!') 
        return 0
    else:
        if (kernel.shape[0] != kernel.shape[1] or kernel.shape[0] != n or kernel.shape[1] != n):
                print('error!') 
                return 0 
        else:
                a = n // 2
                height = img.shape[0]
                width = img.shape[1]
                newimg = np.zeros([height,width])
                for i in range(a,height-a-1):
                        for j in range(a,width-a-1):
                            flag = 1
                            for ii in range(-a,a):
                                    for jj in range(-a,a):
                                            if kernel[a+ii][a+jj] == 1:
                                                    if img[i+ii][j+jj] == 0:
                                                            flag = 0
                            if flag == 1:
                                    newimg[i][j] = 255
        return np.uint8(newimg)                        
def myDilate(img,n,kernel):#膨胀
    if n % 2 != 1:
        print('error!') 
        return 0
    else:
        if (kernel.shape[0] != kernel.shape[1] or kernel.shape[0] != n or kernel.shape[1] != n):
            print('error!')  
            return 0 
        else:
            a = n // 2
            height = img.shape[0]
            width = img.shape[1]
            newimg = np.zeros([height,width])
            for i in range(a,height-a-1):
                for j in range(a,width-a-1):
                        flag = 0
                        for ii in range(-a,a):
                                for jj in range(-a,a):
                                    if kernel[a+ii][a+jj] == 1:
                                        if img[i + ii][j + jj] == 255:
                                            flag = 1
                        if flag == 1:
                            newimg[i][j] = 255
            return np.uint8(newimg)  
def myMorphologyEx(type,img,n,kernel):#开运算和闭运算，使用参数控制具体是哪一个（可以设置迭代次数）
    if type == 0:#开运算
        newimg = img.copy()
        newimg = myErode(newimg,n,kernel)
        newimg = myDilate(newimg,n,kernel)
        return np.uint8(newimg) 
    elif type == 1:#闭运算
        newimg = img.copy()
        newimg = myDilate(newimg,n,kernel)
        newimg = myErode(newimg,n,kernel)
        return np.uint8(newimg) 
    else:
        print('error!')  
        return 0


img = cv2.imread('1.bmp', cv2.IMREAD_GRAYSCALE)
krnl = np.zeros([3,3])
# for i in range(3):
#     krnl[i][1] = 1
# for j in range(3):
#     krnl[1][j] = 1
for i in range(3):
    for j in range(3):
        krnl[i][j] = 1
height,width = img.shape
imgf = img.copy()#二值化
for i in range(height):
    for j in range(width):
        if imgf[i][j] >= 200:
            imgf[i][j] = 255
        else:
            imgf[i][j] = 0
newimg1 = myErode(imgf,3,krnl)
newimg2 = myDilate(imgf,3,krnl)
newimg3 = myMorphologyEx(0,imgf,3,krnl)
newimg4 = myMorphologyEx(1,imgf,3,krnl)
cv2.imshow('image',imgf)
cv2.imshow('1',newimg1)
cv2.imshow('2',newimg2)
cv2.imshow('3',newimg3)
cv2.imshow('4',newimg4)
cv2.waitKey()
cv2.destroyAllWindows()


