import matplotlib.pyplot as plt
import numpy as np
from numpy import fft
import math
import cv2
 
 
def get_motion_psf(image_size, motion_angle, motion_dis): #转换函数H(u,v)
    PSF = np.zeros(image_size)  # 系统点扩散函数
    x_center = (image_size[0] - 1) / 2
    y_center = (image_size[1] - 1) / 2
 
    sin_val = math.sin(motion_angle * math.pi / 180)
    cos_val = math.cos(motion_angle * math.pi / 180)
 
    # 将对应角度上motion_dis个点置成1
    for i in range(motion_dis):
        x_offset = round(sin_val * i) 
        y_offset = round(cos_val * i)
        PSF[int(x_center - x_offset), int(y_center + y_offset)] = 1
 
    return PSF / motion_dis    # 归一化


# 对图片进行运动模糊
def make_blurred(input, PSF, eps):
    input_fft = fft.fft2(input)  # 原图像的傅里叶变换F(u,v)
    PSF_fft = fft.fft2(PSF) + eps
    blurred = fft.ifft2(input_fft * PSF_fft) #G(u,v)=F(u,v)*H(u,v) (最后把G反傅)
    blurred = np.abs(fft.fftshift(blurred))
    return blurred
 
 
def inverse(input, PSF, eps):  # 逆滤波
    input_fft = fft.fft2(input) #对退化图像进行傅里叶变换
    PSF_fft = fft.fft2(PSF) + eps  #点扩散函数进行傅里叶变换
    result = fft.ifft2(input_fft / PSF_fft)  # 逆滤波计算F=G/H  (最后把F反傅)
    result = np.abs(fft.fftshift(result)) #移动中心
    return result
 

def wiener(input, PSF, eps, SNR=0.01):  # 维纳滤波，K=0.01
    input_fft = fft.fft2(input)
    PSF_fft = fft.fft2(PSF) + eps
    PSF_fft_1 = np.conj(PSF_fft) / (np.abs(PSF_fft) ** 2 + SNR)   #这里求H'，conj是求复共轭
    result = fft.ifft2(input_fft * PSF_fft_1)  #（F=H`*G）
    result = np.abs(fft.fftshift(result))
    return result
 
# 显示原图像
image = cv2.imread('1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
img_h = image.shape[0]
img_w = image.shape[1]
plt.xlabel("Original Image")
plt.imshow(image,'gray') 
plt.show()

# 进行运动模糊处理 
PSF = get_motion_psf((img_h, img_w), 60, 10)
blurred = np.abs(make_blurred(image, PSF, 0.01)) 
plt.xlabel("Motion blurred")
plt.imshow(blurred,'gray')
plt.show()
 
# 逆滤波
result = inverse(blurred, PSF, 0.01)
plt.xlabel("inverse deblurred")
plt.imshow(result,'gray')
plt.show()
 
# 维纳滤波
result = wiener(blurred, PSF, 0.01) 
plt.xlabel("wiener deblurred(k=0.01)")
plt.imshow(result,'gray')
plt.show()

# 添加噪声且运动模糊,standard_normal产生随机的函数 
blurred_noisy = blurred + 0.1 * blurred.std() * \
                np.random.standard_normal(blurred.shape) 
plt.xlabel("motion & noisy blurred")
plt.imshow(blurred_noisy,'gray')
plt.show() 

# 噪声+运动模糊的图像 逆滤波
result = inverse(blurred_noisy, PSF, 0.01) 
plt.xlabel("inverse deblurred")
plt.imshow(result,'gray')
plt.show()

# 噪声+运动模糊的图像 维纳滤波 
result = wiener(blurred_noisy, PSF, 0.01)  
plt.xlabel("wiener deblurred(k=0.01)")
plt.imshow(result,'gray') 
plt.show()