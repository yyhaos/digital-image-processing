# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:02:18 2019

@author: TT
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 18:50:35 2019

@author: Administrator
"""

import numpy as np
from PIL import Image
# Laplace算子
# Laplace算子[[0,1,0],[1,-4,1],[0,1,0]] [[1,1,1],[1,-8,1],[1,1,1]]
   
img = Image.open("lena.bmp").convert("L") #转换为灰度图
img.show()
img_array = np.array(img) #转换为矩阵
r = img_array.shape[0]
c = img_array.shape[1]

new_image = np.zeros((r, c)) #初始化
L_suanzi = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])   
#L_suanzi = np.array([[1,1,1],[1,-8,1],[1,1,1]]) 
for i in range(r-2):
    for j in range(c-2):
        new_image[i+1, j+1] = abs(np.sum(img_array[i:i+3, j:j+3] * L_suanzi))
        
img2 = Image.fromarray(np.uint8(new_image))
img2.show()