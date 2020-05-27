import cv2
import numpy as np
import scipy.signal as signal

def LoG(img):
    image_array=np.array(img)
    #LoG算子
    LoG_operator=np.array([[0,0,1,0,0],[0,1,2,1,0],[1,2,-16,2,1],[0,1,2,1,0],[0,0,1,0,0]])
    #像素与算子做卷积，对图像进行平滑处理以及边缘检测
    image_edge=signal.convolve2d(image_array,LoG_operator,mode="same")
    #卷积结果线性变换到0-255
    image_edge=abs(image_edge)
    edge_max=image_edge.max()
    image_edge=(image_edge/edge_max)*255
    #去掉图像外围的边缘点
    rows,cols=img.shape
    image_edge[0:6]=0
    image_edge[rows-6:rows]=0
    image_edge[:,0:6]=0
    image_edge[:,cols-6:cols]=0
    #将小于某一阈值的灰度值变成0，便于观察边缘
    image_edge[image_edge<image_edge.mean()+30]=0
    return image_edge

def hough_line(img):
    #在θ的极值范围内对其等分
    thetas=np.deg2rad(np.linspace(0,360,361)) #将角度转换为对应的弧度
    num_theta=len(thetas)
    cos_t=np.cos(thetas)
    sin_t=np.sin(thetas)

    #在ρ的极值范围内对其等分
    rows,cols=img.shape
    diag_len=np.ceil(np.sqrt(rows**2+cols**2)) #计算img对角线长度
    num_rho=int(diag_len)+1    
    rhos=np.linspace(0,diag_len,num_rho) #ρ的范围[0,对角线]
    
    #新建一个用于统计的二维数组
    vote=np.zeros((num_rho,num_theta),dtype=np.uint64)
    #得到图像上的所有边缘点的索引值
    y_index,x_index=np.nonzero(img)
    #进行交点统计
    for i in range(len(x_index )):
        x=x_index[i]
        y=y_index[i]
        for j in range(num_theta):            
            rho=round(x*cos_t[j]+y*sin_t[j]) #round：四舍五入
            vote[int(rho)][j]+=1
    return vote,rhos,thetas

#读取图像并转换为灰度图
image = cv2.imread("light.jpg")
image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#调用LoG和hough_line函数
image_edge=LoG(image_gray)
vote,rhos,thetas=hough_line(image_edge)
hough_image=image.copy()
rows,cols=image_gray.shape

#找交点
for i in range(len(rhos)):
    for j in range(len(thetas)):
        rho=rhos[i]
        theta=thetas[j]
        if(vote[i][j]>55): #经验阈值
            print("rho={0:.0f}, theta={1:.0f}".format(rho, np.rad2deg(theta)))
            if(theta<(np.pi/4.0))or(theta>(3.0*np.pi/4.0)): #与上下边界相交                
                p1=(int(rho/np.cos(theta)),0) #与第一行的交点		
                p2=(int((rho-rows*np.sin(theta))/np.cos(theta)),rows) #与最后一行的交点                
                cv2.line(hough_image,p1,p2,(255)) #绘制该直线
            else: #与左右边界相交		
                p1=(0,int(rho/np.sin(theta))) #与第一列的交点
                p2=(cols,int((rho-cols*np.cos(theta))/np.sin(theta))) #与最后一列的交点
                cv2.line(hough_image,p1,p2,(255)) #绘制该直线

#显示图像
cv2.imshow("original image",image)
cv2.imshow("edge image",image_edge)
cv2.imshow("hough transform",hough_image)

