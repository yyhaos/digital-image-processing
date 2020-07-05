# -*- coding: utf-8 -*-
"""
Created on Thu May 28 00:25:55 2020

@author: yyhaos
@github: 
"""

import matplotlib.pyplot as plt #用于图片展示
import numpy as np #fft 但是并没有用np的fft，而是自己写了一个dft
import cv2 #读取图片
import os
import warnings
warnings.filterwarnings("ignore")
    
USE_MYDFT = 0  #=1:使用MyDFT    =0:使用np.fft
TEST_PATH = 'test2.jpg'  #可选：DFT_test.jpg  test.jpg   test2.jpg test3.jpg test4.jpg
# test2.jpg的效果最好
C  =2
DD  = 100000
RL = 0.25
RH = 4
#4 个 同态滤波的参数


class MyDFT(): 
#    DFT实现
    def idft(self,F):
#       逆dft 参考课本 P128 ,dip6 P47
        (M,N) = F.shape #M,N对应 dip6 P47 的M,N
        f = np.zeros(F.shape , np.complex) #f对应 dip6 P47 下面式子中的的f
#        f暂时是个虚数数组，但其实它的所有数的虚部理应是0 （逆变换后是实数,不过因为double的精度问题，所以变不了0）
        for u in range(M):
            for v in range(N):
#                u,v对应dip6 P47 下面那个式子的u,v
#                print(u,v)
                print('\r',1.0*((u+1)*N+(1+v))/M/N *100,"%\r",end='\r',flush=True )
                for x in range(M): 
                    for y in range(N):
                        du = 2*np.pi*(1.0*u*x/M  + 1.0*v*y/N) #记录一下偏转的弧度
                        f[u][v] += F[x][y]*(np.cos(du) + np.sin(du)*1.j) # 对应式子里的求和
#                        F[x][y] 对应F(x,y)
#                         j = sqrt(-1) ,应用欧拉公式,得到 e = cos(du) + i *sin(du)
#                        np.cos(du) + np.sin(du)*1.j对应 e^(j*2*PI*(ux/M+vy/N))
#        print("yyy\n",f,"yyy\n")
        
        result = np.real(np.exp(f.real) - 0.01)    
        return result
    def dft(self,input): 
        input = np.log(input + 0.01)
#        dft 参考课本128 ,dip6 P47
#        input = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY) #灰度化
        f = np.double(input)  #先转化为double型 这样就得到了初始的f， f对应dip6 P47 上面那个式子的f        
#        print("原始数据:",f)
        (M,N) = f.shape #得到M,N， M是图片高度，N是图片宽度，应dip6 P47 上面的M\N
        F = np.zeros(f.shape, dtype = np.complex) #对应对应dip6 P47 上面那个式子的F, 大小为f的大小、初始化为0
#        F是一个复数数组
        for u in range(M):
            for v in range(N):
#                u,v对应dip6 P47 上面那个式子的u,v
#                print(u,v)
                print('\r',"{:.4}".format(1.0*((u+1)*N+(1+v))/M/N *100),"%\r",end='\r',flush=True )
                for x in range(M):
                    for y in range(N):
                        du = 2*np.pi*(1.0*u*x/M  + 1.0*v*y/N)#记录一下偏转的弧度
                        F[u][v] += f[x][y]*(np.cos(-du) + np.sin(-du)*1.j) # 对应式子里的求和
#                        f[x][y] 对应 f(x,y) 
#                         j = sqrt(-1) ,应用欧拉公式,得到 e = cos(-du) + i *sin(-du)
#                        (np.cos(-du) + np.sin(-du)*1.j) 对应 e^(-j*2*PI*(ux/M+vy/N))
#        print("xxx\n",F,"xxx\n")
        return F/M/N
    
class NpFFT():
#    numpy的FFT实现，套了一个壳子
    def fft(self,input):
        input = np.log(input + 0.01)
        return np.fft.fft2(input)
    def ifft(self, input):
        input = np.fft.ifft2(input) 
        input = np.real(np.exp(input) - 0.01) 
        return input

class MyHomomorphicFilter(): #同态滤波器实现
    def homofilter(self, image):
        c = C   #常数c用于控制坡度的锐利度，它在rl和rh之间过渡
        D0 = DD
        rh = RH 
        rl = RL
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
        return  np.fft.ifftshift(H)
    
def show(input,title="image"):
    plt.rcParams['figure.dpi'] = 120
    plt.xlabel(title)
    try:
        #print("start imshow:"+title)
        plt.imshow( (input*100000).astype(int),'gray') 
        plt.savefig('result//'+title)
        plt.show()
        #print("end imshow:"+title)    
    except:
        print("error in show or save image:"+title)
        
def main():
    try:
        os.mkdir('result')
    except:
        1
    
    image = cv2.imread(TEST_PATH)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #灰度化
    image = np.double(image)  #先转化为double型 这样就得到了初始的image
    
    show( image,"Original test image" )
    
    mydft=MyDFT()
    npfft=NpFFT()
    hf=MyHomomorphicFilter()
 
    if(USE_MYDFT==1):
        dft_image = mydft.dft(image)
    else:
        dft_image = npfft.fft(image)
    show( dft_image,"Test image after dft" )
    
    
    
    hf_image= hf.homofilter(dft_image)
    show(hf_image, "Image of homofilter")
    
    hf_image = hf_image*dft_image
    show(hf_image, "Test image after homofilted")
    
    if(USE_MYDFT==1):
        ifft_image = mydft.idft(hf_image) 
    else:
        ifft_image = npfft.ifft(hf_image) 
    
    
    show(ifft_image,"Test image after idft")
    

if __name__ =='__main__':
    main()