#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 生成图片对应的直方图
def HistBar(pic):
	bins = np.arange(257)
	item = pic[:, :]
	
	hist, bins = np.histogram(item, bins)
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[ : -1] + bins[1 : ]) / 2

	plt.bar(center, hist, align = 'center', width = width)
	plt.show()

# 读取图片并显示
uneq = cv.imread('Uneque.jpg', 0)
cv.imshow("ori",uneq)
HistBar(uneq)

# 直方图均衡化
hist, bins = np.histogram(uneq.flatten(), 256, [0, 256])

cdf = hist.cumsum()
cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = cdf_m * 255 / cdf_m.max()
cdf = np.ma.filled(cdf_m, 0).astype('uint8')

result = cdf[uneq]
cv.imshow("result", result)
HistBar(result)

# 图片检验
check = cv.equalizeHist(uneq)
cv.imshow("check",check)
HistBar(check)

cv.waitKey(0)
cv.destroyAllWindows()