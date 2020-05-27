import matplotlib.pyplot as plt
import numpy as np

def Morphologychange(img,fil,mode):                 #分别提取三个通道
    h = fil.shape[0] // 2
    w = fil.shape[1] // 2
    img = np.pad(img, ((h, h), (w, w),(0, 0)), 'constant')
    conv_b = _change(img[:,:,0],fil,mode)           #然后进行卷积操作
    conv_g = _change(img[:,:,1],fil,mode)
    conv_r = _change(img[:,:,2],fil,mode)
    dstack = np.dstack([conv_b,conv_g,conv_r])      #将卷积后的三个通道合并
    return dstack                                   #返回卷积后的结果


def _change(img,fil,mode):             
    fil_heigh = fil.shape[0]                        #获取卷积核的高度
    fil_width = fil.shape[1]                        #获取卷积核的宽度    
    conv_heigh = img.shape[0] - fil.shape[0] + 1    #确定卷积结果的大小
    conv_width = img.shape[1] - fil.shape[1] + 1
    conv = np.zeros((conv_heigh,conv_width),dtype = 'uint8')
    if mode == 1:                                   #膨胀操作
        for i in range(conv_heigh-1):
            for j in range(conv_width-1):           #逐点计算
                conv[i+1][j+1]= np.max(img[i:i + fil_heigh,j:j + fil_width ])
    if mode == 2:                                   #腐蚀操作
        for i in range(conv_heigh-1):
            for j in range(conv_width-1):           #逐点计算
                conv[i+1][j+1]= np.min(img[i:i + fil_heigh,j:j + fil_width ])
    return conv


img = plt.imread("pic.jpg")                         #在这里读取图片
fil = np.ones((5,5),np.float32)                     #定义卷积核
res = Morphologychange(img,fil,1)
plt.imsave("Dilation.jpg",res)
res = Morphologychange(img,fil,2)
plt.imsave("Erosion.jpg",res)
