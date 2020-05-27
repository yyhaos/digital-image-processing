import cv2
import numpy as np

# 读入图片，第一张是彩色原图，第二张是绝对前景
img = cv2.imread('1.bmp')
fore = cv2.imread('definateFore.bmp',cv2.IMREAD_GRAYSCALE)
back = cv2.imread('definateBack.bmp',cv2.IMREAD_GRAYSCALE)
trimap = cv2.imread('1.bmp',cv2.IMREAD_GRAYSCALE)
global estimated_img_fore,estimated_img_back
# 前景的估计
estmt_img_fore = img.copy()
# 后景的估计
estmt_img_back = img.copy()
global estimated_img
global flag 
flag = 0
eps = 1e-8


# 求出分析模板，绝对前景1，绝对后景0，未知2
def getform(trimap, fore, back):
    form = np.zeros([trimap.shape[0],trimap.shape[1]])
    for i in range(trimap.shape[0]):
        for j in range(trimap.shape[1]):
            if back[i][j] == 255:
                form[i][j] = 2
            if fore[i][j] == 255:
                form[i][j] = 1
    return form


# 求出估计值图像用于计算alpha
def estimate(img, form):
    for chnl in range(3):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if form[i][j] == 1:
                    estmt_img_back[i][j][chnl] = 0
                elif form[i][j] == 0:
                    estmt_img_fore[i][j][chnl] = 0
                elif form[i][j] == 2:
                    r = 1
                    isFore = 0
                    isBack = 0
                    while (isFore == 0 or isBack == 0):
                        for ii in range(max(0,i-r),min(img.shape[0],i+r)):
                            for jj in range(max(0,j-r), min(img.shape[1],j+r)):
                                if isFore == 0:
                                    if form[ii][jj] == 1:
                                        isFore = 1
                                        estmt_img_fore[i][j][chnl] = img[ii][jj][chnl]
                                if isBack == 0:
                                    if form[ii][jj] == 0:
                                        isBack = 1
                                        estmt_img_back[i][j][chnl] = img[ii][jj][chnl]
                        r += 1


def poisson_init(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    minus = img.copy()
    for chnl in range(3):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                minus[i][j][chnl] = int(estmt_img_fore[i][j][chnl]) - int(estmt_img_back[i][j][chnl])
    minus_gray = cv2.cvtColor(minus, cv2.COLOR_RGB2GRAY)
    float_minus_gray = np.float32(minus_gray)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if float_minus_gray[i][j] - 0 <= eps:
                float_minus_gray[i][j] = 0.001
    back_gray = cv2.cvtColor(estmt_img_back, cv2.COLOR_RGB2GRAY)
    estimated_alpha = np.zeros([img_gray.shape[0],img_gray.shape[1]])
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            estimated_alpha[i][j] = 100*(int(img_gray[i][j]) - int(back_gray[i][j]))/float(float_minus_gray[i][j])
    return estimated_alpha


def poisson(img, old_alpha):
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    minus = img.copy()
    for chnl in range(3):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                minus[i][j][chnl] = int(estmt_img_fore[i][j][chnl]) - int(estmt_img_back[i][j][chnl])
    minus_gray = cv2.cvtColor(minus,cv2.COLOR_RGB2GRAY)
    minus_gray = np.float32(minus_gray)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if minus_gray[i][j] - 0 <= eps:
                minus_gray[i][j] = 0.001

    new_alpha = np.zeros([img.shape[0],img.shape[1]])
    new_alpha = np.float32(new_alpha)
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            divI = ((int(img_gray[i+1][j])+int(img_gray[i-1][j])-2*int(img_gray[i][j]))*float(minus_gray[i,j])-int(img_gray[i+1][j])-int(img_gray[i][j]))*(float(minus_gray[i+1,j])-float(minus_gray[i,j]))/(float(minus_gray[i,j])**2)
            divJ = ((int(img_gray[i][j+1])+int(img_gray[i][j-1])-2*int(img_gray[i][j]))*float(minus_gray[i,j])-int(img_gray[i][j+1])-int(img_gray[i][j]))*(float(minus_gray[i,j+1])-float(minus_gray[i,j]))/(float(minus_gray[i,j])**2)
            div = divI + divJ
            new_alpha[i][j] = 100.0*(float(old_alpha[i+1][j])/100.0+float(new_alpha[i-1][j])/100.0+float(old_alpha[i][j+1])/100.0+float(new_alpha[i][j-1])/100.0-div)/4.0
    return new_alpha


def renew_form(new_alpha, form):
    change_count = 0
    unknown_count = 0
    for i in range(form.shape[0]):
        for j in range(form.shape[1]):
            if new_alpha[i][j] > 95:
                if form[i][j] != 1:
                    form[i][j] == 1
                    change_count += 1
            elif new_alpha[i][j] <5:
                if form[i][j] != 0:
                    form[i][j] == 0
                    change_count += 1
    if change_count == 0:
        flag = 1
    return form


def output(form,img):
    height = img.shape[0]
    width = img.shape[1]
    channel = img.shape[2]
    finished_img = np.zeros([height,width,channel])
    for chnl in range(3):
        for i in range(height):
            for j in range(width):
                if form[i][j] == 1:
                    finished_img[i][j][chnl] = img[i][j][chnl]
    return np.uint8(finished_img)


def main():
    #cv2.imshow('img',img)
    form = getform(trimap, fore, back)
    estimate(img,form)
    old_alpha = poisson_init(img)
    new_alpha = poisson(img, old_alpha)
    form = renew_form(new_alpha, form)
    i = 0
    while (i <= 2):
        new_alpha = poisson(img, new_alpha)
        form = renew_form(new_alpha, form)
        estimate(img, form)
        i += 1
    finished_img = output(form, img)
    cv2.imshow('estmt_img_fore',estmt_img_fore)
    cv2.imshow('estmt_img_back',estmt_img_back)
    cv2.imshow('finished_img', finished_img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()