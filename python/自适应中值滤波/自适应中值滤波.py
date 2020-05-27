import cv2 as cv 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def PepperandSalt(src,percetage):
    NoiseImg=src
    NoiseNum=int(percetage*src.shape[0]*src.shape[1])
    for i in range(NoiseNum):
        randX=np.random.randint(0,src.shape[0]-1)
        randY=np.random.randint(0,src.shape[1]-1)
        if np.random.random()<=0.5:
            NoiseImg[randX,randY]=0
        else:
            NoiseImg[randX,randY]=255          
    return NoiseImg
def adaptiveProcess(tempImg, i, j, ks, Smax):
    pixels = []
    k = int(ks/2)
    for a in (-k,k):
        for b in (-k,k):
            pixels.append(tempImg[i+a,j+b])
    Zmin = min(pixels)
    Zmax = max(pixels)
    Zmed = np.median(pixels)
    Zxy = tempImg[i,j]

    if(Zmed>Zmin and Zmed<Zmax):
        if(Zxy>Zmin and Zxy<Zmax):
            return Zxy
        else:
            return Zmed
    else:
        ks += 2
        if(ks<=Smax):
            return adaptiveProcess(tempImg, i, j, ks, Smax)
        else:
            return Zmed


if __name__ == "__main__":
    #图片读取并转化为灰度图
    filename='circuit.jpg'
    img = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    noiseImg=img.copy()
    #椒盐化
    noiseImg=PepperandSalt(noiseImg,0.1)
    #滤波器窗口的起始、最大尺寸
    Smin=3
    Smax=7
    #扩展图像边界
    tempImg = cv.copyMakeBorder(noiseImg,int(Smax/2),int(Smax/2),int(Smax/2),int(Smax/2),cv.BORDER_REFLECT)
    
    #图像处理
    half=int(Smax/2)
    rows,cols=tempImg.shape
    #print('start')
    for i in range(half,rows-half):
        for j in range(half,cols-half):
            tempImg[i,j]=adaptiveProcess(tempImg, i, j, Smin, Smax)
    #print('end')
    dst = tempImg[half:rows+half,half:cols+half]


    #show
    plt.subplot(1,2,1)
    plt.title('PepperandSalt')
    plt.imshow(noiseImg,cmap="gray")
    plt.axis('off')
    plt.subplot(1,2,2)
    plt.title('adaptiveProcess')
    plt.imshow(dst,cmap="gray")
    plt.axis('off')
    plt.show()


