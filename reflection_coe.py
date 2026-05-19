import json
import re
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import os.path
class reflection_coe(QMainWindow):
    def __init__(self):
        super(reflection_coe, self).__init__()
        self.setWindowTitle("Set Reflection Coefficient")
        self.file_name = "__data.png"
        if os.path.isfile(self.file_name) == False:
            QMessageBox.warning(self, "Warning", "Please draw an image first!", QMessageBox.Yes | QMessageBox.Discard)
            return
        self.setupUi(self)
        self.retranslateUi(self)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(615, 163)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(5, 15, 600, 111))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_5 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(self.splitter)
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit.raise_()
        self.pushButton.raise_()
        self.label_5.raise_()
        img = cv2.imread(self.file_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        num, res = cv2.connectedComponents(gray)
        self.num = num
        self.pushButton.clicked.connect(self.process)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Set Reflection Coefficient"))
        self.label_5.setText(_translate("Form", "Enter {} reflection coefficients (separated by space):".format(self.num-1)))
        self.pushButton.setText(_translate("Form", "OK"))
    def process(self):
        xishu = self.lineEdit.text()
        self.xishu = re.findall(r'-?\d+\.?\d*e?-?\d*?',xishu)
        for i in list(self.xishu):
            i = float(i)
            if i <= float(-1) or i >= float(1):
                QMessageBox.warning(self, " ", "Reflection coefficient error, range should be -1 to 1", QMessageBox.Yes | QMessageBox.Discard)
                return
        if len(self.xishu) == int(self.num-1):
            fjson = 'project.json'
            with open(fjson, 'r') as f:
                content = json.load(f)
            axis = {"xishu": self.xishu}
            content.update(axis)
            with open(fjson, 'w') as f_new:
                json.dump(content, f_new)
            QMessageBox.warning(self, " ", "Reflection coefficient saved successfully",  QMessageBox.Yes| QMessageBox.Discard)
        else:
            QMessageBox.warning(self, " ", "Number of layers does not match number of coefficients, please enter again", QMessageBox.Yes | QMessageBox.Discard)




