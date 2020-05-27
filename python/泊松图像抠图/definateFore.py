import cv2
import numpy as np
 
# -----------------------鼠标操作相关------------------------------------------
lsPointsChoose = []
tpPointsChoose = []
pointsCount = 0
count = 0
pointsMax = 40
def on_mouse(event, x, y, flags, param):
    global img, point1, count, pointsMax
    global lsPointsChoose, tpPointsChoose  # 存入选择的点
    global pointsCount  # 对鼠标按下的点计数
    global img2, ROI_bymouse_flag
    img2 = img.copy()  # 此行代码保证每次都重新再原图画  避免画多了

 
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        pointsCount = pointsCount + 1
        point1 = (x, y)
        # 画出点击的点
        cv2.circle(img2, point1, 10, (0, 255, 0), 2)
 
        # 将选取的点保存到list列表里
        lsPointsChoose.append([x, y])  # 用于转化为darry 提取多边形ROI
        tpPointsChoose.append((x, y))  # 用于画点
        # ----------------------------------------------------------------------
        # 将鼠标选的点用直线连起来
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(img2, tpPointsChoose[i], tpPointsChoose[i + 1], (255, 0, 0), 2)
        # ----------------------------------------------------------------------
        # ----------点击到pointMax时可以提取去绘图----------------
        if (pointsCount == pointsMax):
            # -----------绘制感兴趣区域-----------
            ROI_byMouse()
            ROI_bymouse_flag = 1
            lsPointsChoose = []
        cv2.imshow('src', img2)
    # ----------点击到pointMax时可以提取去绘图----------------
    if event == cv2.EVENT_MBUTTONDOWN:
        # -----------绘制感兴趣区域-----------
        ROI_byMouse()
        ROI_bymouse_flag = 1
        lsPointsChoose = []
    # -------------------------右键按下清除轨迹-----------------------------
    if event == cv2.EVENT_RBUTTONDOWN:  # 右键点击
        print("right-mouse")
        pointsCount = 0
        tpPointsChoose = []
        lsPointsChoose = []
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(img2, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
        cv2.imshow('src', img2)
 
def ROI_byMouse():
    global src, ROI, ROI_flag, mask2
    mask = np.zeros(img.shape, np.uint8)
    pts = np.array([lsPointsChoose], np.int32)  # pts是多边形的顶点列表（顶点集）
    pts = pts.reshape((-1, 1, 2))
    # 这里 reshape 的第一个参数为-1, 表明这一维的长度是根据后面的维度的计算出来的。
    # OpenCV中需要先将多边形的顶点坐标变成顶点数×1×2维的矩阵，再来绘制
 
    # --------------画多边形---------------------
    mask = cv2.polylines(mask, [pts], True, (255, 255, 255))
    ##-------------填充多边形---------------------
    mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))
    cv2.imshow('mask', mask2)
    cv2.imwrite('definateFore.bmp', mask2)
    ROI = cv2.bitwise_and(mask2, img)
    cv2.imwrite('definateForeROI.bmp', ROI)
    cv2.imshow('ROI', ROI)
 
 

 
 
img = cv2.imread('1.bmp')
ROI = img.copy()
cv2.namedWindow('src')
cv2.setMouseCallback('src', on_mouse)
cv2.imshow('src', img)
cv2.waitKey(0)
cv2.destroyAllWindows()