import cv2 as cv
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *


class opencv(QDialog):
    def __init__(self,type):
        # Initialize ndarray for image storage
        self.img = np.ndarray(())
        super().__init__()
        self.type = type
        self.initUI(type)
    def initUI(self,type):
        # Set window icon
        # self.setWindowIcon(QIcon("filename"))
        # Set window title
        self.setWindowTitle("{} Edge Detection".format(type))
        self.resize(400, 300)
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)
        self.label = QLabel()
        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnProcess, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)
        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)
    def openSlot(self):
        # 调用打开文件diglog

        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if fileName == '':
            return
        # 采用opencv函数读取数据
        self.img = cv.imread(fileName, -1)
        if self.img.size == 1:
            return
        self.refreshShow()
    def saveSlot(self):
        if self.img.size == 1:
            QMessageBox.warning(self, "警告", "请先选择图片！", QMessageBox.Yes | QMessageBox.No)
            return
        # Save file dialog
        fileName = '__data.png'
        '''
        fileName, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', './__data', '*.png *.jpg *.bmp', '*.png')
        '''
        if fileName == '':
            return

        # 调用opencv写入图像
        cv.imwrite(fileName, self.img)
        QMessageBox.warning(self, " ", "识别后的图像保存成功", QMessageBox.Yes | QMessageBox.Discard)
    def processSlot(self):
        if self.img.size == 1:
            QMessageBox.warning(self, "Warning", "Please select an image first!", QMessageBox.Yes | QMessageBox.No)
            return
        maping = {
            'Scharr Operator':self.Scharr(),
            'Sobel Operator':self.Sobel(),
            'Laplacian Operator':self.Log(),
            'Canny Edge Detection': self.Canny(),
        }
        self.img = maping.get(self.type)
        self.refreshShow()
    def refreshShow(self):
        # Extract image dimensions and channels for conversion from OpenCV to QImage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        self.label.setPixmap(QPixmap.fromImage(self.qImg))
    def Sobel(self):
        x = cv2.Sobel(self.img, cv2.CV_16S, 1, 0)
        y = cv2.Sobel(self.img, cv2.CV_16S, 0, 1)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        dst_sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        return dst_sobel
    def Scharr(self):
        x = cv2.Scharr(self.img, cv2.CV_16S, 1, 0)  # X direction
        y = cv2.Scharr(self.img, cv2.CV_16S, 0, 1)  # Y direction
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        dst_scharr = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        return dst_scharr
    def Log(self):
        dst = cv2.Laplacian(self.img, cv2.CV_16S, ksize=3)
        dst_log = cv2.convertScaleAbs(dst)
        return dst_log
    def Canny(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
        eroded = cv2.erode(self.img,kernel)
        edge_output = cv.Canny(eroded, 0, 150)
        dst_canny = cv.bitwise_and(self.img, self.img, mask=edge_output)
        return dst_canny



