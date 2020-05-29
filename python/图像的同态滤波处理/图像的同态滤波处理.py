import matplotlib.pyplot as plt
import numpy as np
from numpy import fft
import math
import cv2
 
def homofilter(input):
    input = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY) #灰度化
    imagepre = np.double(input)  #先转化为double型
    
    Firstlog = np.log(imagepre + 1)  #第一步取对数(+0.01保证log真数都大于0)
    Secondfft = np.fft.fft2(Firstlog)   #第二步傅里叶变换
    
    #第三步设计滤波器
    c = 1   #常数c用于控制坡度的锐利度，它在rl和rh之间过渡
    D0 = 80
    rh = 1 
    rl = 0.25
    h = image.shape[0]
    w = image.shape[1]
    h1 = np.floor(h/2)
    w1 = np.floor(w/2)
    D = np.zeros((h,w)) 
    H = np.zeros((h,w)) 
    M = np.zeros((h,w)) 
    for i in range(h):
        for j in range(w):
            D[i,j] = (i - h1)**2 + (j - w1)**2
            M[i,j] = 1 - np.exp(-c * (D[i,j]/(D0**2)))
            H[i,j] = (rh - rl) * M[i,j] + rl 
    
    #第四步用上述滤波器处理原图像，结果反傅里叶变换
    H = np.fft.ifftshift(H)  #上面产生的是中心化滤波器，而图像未中心化，所以这里要将滤波器反中心化
    Fourthifft = np.fft.ifft2(H * Secondfft) 
    
    #第五步 取指数再减回去最初加的,  #取实部
    result = np.real(np.exp(Fourthifft) - 1) 

    return result
            

#显示原图像  
plt.rcParams['figure.dpi'] = 120
image = cv2.imread('2.jpg')
plt.xlabel("Original Image")
plt.imshow(image,'gray') 
plt.show()

#显示同态滤波处理后图像
result = homofilter(image)
plt.xlabel("Afterhomofilter")
plt.imshow(result,'gray')
plt.show()    
