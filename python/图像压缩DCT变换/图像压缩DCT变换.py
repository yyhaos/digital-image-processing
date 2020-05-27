import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt
#导入图像 
path='lena.png'
img = cv2.imread(path,0)
img = img.astype('float')
#print(img.shape)
#参数初始化 
m,n = img.shape
N=8
mask = [1,1,1,1,0,0,0,0,\
        1,1,1,0,0,0,0,0,\
        1,1,0,0,0,0,0,0,\
        1,0,0,0,0,0,0,0,\
        0,0,0,0,0,0,0,0,\
        0,0,0,0,0,0,0,0,\
        0,0,0,0,0,0,0,0,\
        0,0,0,0,0,0,0,0]
mask = np.array(mask).reshape(8,8)
C_temp = np.zeros((N,N))
dst = np.zeros(img.shape) 
yasuo = np.zeros(img.shape) 
img_recor = np.zeros(img.shape) 
img_yasuo = np.zeros(img.shape) 
C_temp[0, :] = 1 * np.sqrt(1/N)
for i in range(1, N):
     for j in range(N):
          C_temp[i, j] = np.cos(np.pi * i * (2*j+1) / (2 * N )) * np.sqrt(2 / N )

hdata = np.vsplit(img,n/N) # 垂直分成高度度为8 的块
for i in range(0, n//N):
    blockdata = np.hsplit(hdata[i],m/N) 
    #垂直分成高度为8的块后,在水平切成长度是8的块, 也就是8x8 的块
    for j in range(0, m//N):
        block = blockdata[j]
        a = N*i
        aa = a+N
        b = N*j
        bb = b+N

        temp1 = np.dot(C_temp , block)
        dst[a:aa,b:bb] = np.dot(temp1, np.transpose(C_temp))
        
        yasuo[a:aa,b:bb] = mask*dst[a:aa,b:bb]

        temp2 = np.dot(np.transpose(C_temp) , dst[a:aa,b:bb])
        img_recor[a:aa,b:bb] = np.dot(temp2, C_temp)

        temp3 = np.dot(np.transpose(C_temp) , yasuo[a:aa,b:bb])
        img_yasuo[a:aa,b:bb] = np.dot(temp3, C_temp) 
        
         
# img_dct = cv2.dct(img)         #进行离散余弦变换
# img_recor2 = cv2.idct(img_dct)    #进行离散余弦反变换
# print("dct:",(abs(dst - img_dct) < 0.000001).all())



#SHOW PIC
plt.subplot(141)
plt.imshow(img, 'gray')
plt.title('original image')
plt.xticks([]), plt.yticks([])
 
plt.subplot(142)
plt.imshow(dst,'gray')
plt.title('DCT')
plt.xticks([]), plt.yticks([])
 
 
plt.subplot(143)
plt.imshow(img_recor, 'gray')
plt.title('IDCT')
plt.xticks([]), plt.yticks([])

plt.subplot(144)
plt.imshow(img_yasuo, 'gray')
plt.title('compress')
plt.xticks([]), plt.yticks([])
plt.show()