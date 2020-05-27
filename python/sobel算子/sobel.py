from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#读取图像并显示
img=np.array(Image.open('sample.bmp'))
plt.imshow(img,cmap='Greys_r')
plt.axis('off')
plt.show()
print(img.shape)

rows,cols=img.shape
res=np.zeros((rows,cols))
#Sobel算子对应的模板
#tip1：[[...],[...],[...]]的类型是list，不能直接用于运算
sobel_x=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
sobel_y=np.array([[-1,-2,1],[0,0,0],[1,2,-1]])
#为防止越界，从第二个到倒数第二个
for i in range(1,(rows-1)):
    for j in range(1,(cols-1)):
        #取每个像素点3*3领域的子矩阵
        submatrix=np.array([[img[i-1,j-1],img[i-1,j],img[i-1,j+1]],\
                   [img[i,j-1],img[i,j],img[i,j+1]],\
                   [img[i+1,j-1],img[i+1,j],img[i+1,j+1]]])
        #tip2：sum(sum(y)) 求矩阵y所有元素的和        
        x=sum(sum(submatrix*sobel_x))#计算x方向的微分
        y=sum(sum(submatrix*sobel_y))#计算y方向的微分
        #为简化梯度的计算，使用绝对值之和作近似值
        res[i][j]=abs(x)+abs(y)

#灰度变换：将图像像素值线性变换到 0...255 区间
res_max=res.max()
res=(255/res_max)*res

#显示图像梯度/边缘
plt.imshow(res,cmap='Greys_r')
plt.axis('off')
plt.show()