import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import segmentation as seg
import cv2
from skimage.filters import gaussian


class BtnLabel(QLabel):
    def __init__(self, fname = None, parent=None):
        super(BtnLabel, self).__init__(parent)
        self.if_mouse_press = False
        self.fname = fname

    def mousePressEvent(self, e):
        print('mousePressEvent(%d,%d)\n' % (e.pos().x(), e.pos().y()))
        self.if_mouse_press = True
        points = seg.circle_points(200, [e.pos().x(), e.pos().y()], 200)[:-1]
        im = cv2.imread(self.fname)
        image_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
        cv2.circle(im, (e.pos().x(), e.pos().y()), 200, (255, 0, 0), 3)  # 修改最后一个参数
        snake = seg.active_contour(image_gray, points, alpha=0.015, beta=0.1, gamma=0.001)
        for point in snake:
            cv2.circle(im, (int(point[0]), int(point[1])), 1, (0, 0, 255), 3)  # 修改最后一个参数
        cv2.imwrite('a.jpg', im, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        fname = 'a.jpg'
        self.setPixmap(QPixmap(fname))

    def mouseReleaseEvent(self, e):
        print('mouseReleaseEvent(%d,%d)\n' % (e.pos().x(), e.pos().y()))
        self.if_mouse_press = False

class filedialogdemo(QWidget):

    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent)
        layout = QVBoxLayout()
        self.btn = QPushButton()
        self.btn.clicked.connect(self.loadFile)
        self.btn.setText("选择图片")
        layout.addWidget(self.btn)
        self.label = BtnLabel()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.resize(500, 400)

    def loadFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        im = cv2.imread(fname)
        x, y = im.shape[0:2]
        im = cv2.resize(im, (int(800*float(y)/x), 800))
        cv2.imwrite('after.jpg', im, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        self.label.setPixmap(QPixmap('after.jpg'))
        self.label.fname = 'after.jpg'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileload =  filedialogdemo()
    fileload.show()
    sys.exit(app.exec_())



