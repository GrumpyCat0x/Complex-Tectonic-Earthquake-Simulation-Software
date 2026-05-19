
from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter,\
    QComboBox, QLabel, QSpinBox, QFileDialog
from PaintBoard import PaintBoard
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QColor
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel
import cv2 as cv
class MainWidget(QWidget):


    def __init__(self, Parent=None):
        ''' Constructor '''
        super().__init__(Parent)
        
        self.__InitData() #先初始化数据，再初始化界面
        self.__InitView()
    
    def __InitData(self):
        ''' Initialize member variables '''
        self.__paintBoard = PaintBoard(self)
        # Get color list (string type)
        self.__colorList = QColor.colorNames() 
        
    def __InitView(self):
        ''' Initialize UI '''
        self.setFixedSize(650, 475)
        self.setWindowTitle("PaintBoard Example PyQt5")
        
        # Create horizontal layout for main window
        main_layout = QHBoxLayout(self) 
        # Set layout margins and spacing to 10px
        main_layout.setSpacing(10) 
    
        # Place canvas on the left side
        main_layout.addWidget(self.__paintBoard) 
        
        # Create vertical sub-layout for buttons
        sub_layout = QVBoxLayout() 
        
        # Set sub-layout margins and spacing to 10px
        sub_layout.setContentsMargins(10, 10, 10, 10) 

        self.__btn_Clear = QPushButton("Clear Canvas")
        self.__btn_Clear.setParent(self) # Set parent widget
       
        # Connect button signal to clear function
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear) 
        sub_layout.addWidget(self.__btn_Clear)
        
        # Quit button (commented out)
        # self.__btn_Quit = QPushButton("Quit")
        # self.__btn_Quit.setParent(self) # Set parent widget
        # self.__btn_Quit.clicked.connect(self.Quit)
        # sub_layout.addWidget(self.__btn_Quit)
        
        self.__btn_Save = QPushButton("Save Image")
        self.__btn_Save.setParent(self)
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        sub_layout.addWidget(self.__btn_Save)
        
        self.__cbtn_Eraser = QCheckBox(" Use Eraser")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        sub_layout.addWidget(self.__cbtn_Eraser)
        
        splitter = QSplitter(self) #占位符
        sub_layout.addWidget(splitter)
        
        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("Brush Thickness")
        self.__label_penThickness.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penThickness)
        
        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setMaximum(20)
        self.__spinBox_penThickness.setMinimum(2)
        self.__spinBox_penThickness.setValue(10) #默认粗细为10
        self.__spinBox_penThickness.setSingleStep(2) #最小变化值为2
        self.__spinBox_penThickness.valueChanged.connect(self.on_PenThicknessChange)#关联spinBox值变化信号和函数on_PenThicknessChange
        sub_layout.addWidget(self.__spinBox_penThickness)
        
       # self.__label_penColor = QLabel(self)
       # self.__label_penColor.setText("画笔颜色")
       # self.__label_penColor.setFixedHeight(20)
      #  sub_layout.addWidget(self.__label_penColor)
        
        #self.__comboBox_penColor = QComboBox(self)
       # self.__fillColorList(self.__comboBox_penColor) #用各类颜色填充下拉列表
        #self.__comboBox_penColor.currentIndexChanged.connect(self.on_PenColorChange) #关联下拉列表的当前索引变动信号与函数on_PenColorChange
      #  sub_layout.addWidget(self.__comboBox_penColor)

        main_layout.addLayout(sub_layout) #将子布局加入主布局


    def __fillColorList(self, comboBox):

        index_black = 0
        index = 0
        for color in self.__colorList: 
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70,20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix),None)
            comboBox.setIconSize(QSize(70,20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)
        
   # def on_PenColorChange(self):
   #     color_index = self.__comboBox_penColor.currentIndex()
    #    color_str = self.__colorList[color_index]
  #      self.__paintBoard.ChangePenColor(color_str)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)
    
    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath[0])
        
    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True # Enter eraser mode
        else:
            self.__paintBoard.EraserMode = False # Exit eraser mode
        
        
    #def Quit(self):
    #    self.close()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWidget()#MainWindow()就是绘画板的主函数
  window.move(120, 120)
  window.show()
  app.exec_()