import numpy as np
import sys
import cv2
import PIL
from PIL import ImageGrab, ImageQt, ImageFilter, ImageEnhance
# from PIL.ImageQt import ImageQt

from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtCore import Qt
from screeninfo import get_monitors
import main 

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, monitor_number=None, screen_width=None, screen_height=None, shot=None):
        # TODO Change monitor variables to *args, maybe
        super().__init__(parent)
        # QtWidgets.QMainWindow.__init__(self, parent) probably not needed

        self.monitor_number = int(monitor_number) - 1 #Qt is starting reading screen number from 0
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)
        self.shot = shot
        # no idea why it is here
        # self.screenshot_tool_widget = Screenshot_tool(parent=self)
        # self.setCentralWidget(self.screenshot_tool_widget)

        self.starter()

    def starter(self):
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        # self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #no title bar
        # self.setWindowOpacity(0.3) window transparency
        self.monitor = QtWidgets.QDesktopWidget().screenGeometry(self.monitor_number)
        self.move(self.monitor.left(), self.monitor.top())
        # self.shot = self.shot.point(lambda p: p * 0.9)
        # # ImageFilter.GaussianBlur(radius=2) 
        # self.shot = self.shot.filter(ImageFilter.GaussianBlur(radius=1))
        # enhancer = ImageEnhance.Contrast(self.shot)
        # self.shot = enhancer.enhance(4.0)

        self.qimage = ImageQt.ImageQt(self.shot)

        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap.fromImage(self.qimage)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.show()

    def keyPressEvent(self, event): #q for exit
        if event.key() == QtCore.Qt.Key_Q:
            # print('Quit')
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.start = event.pos()
        # print(main.widget.INSTANCES)
        print(self.start)
        # self.end = self.start
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        print(self.end)
        self.update()





# class Screenshot_tool(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         QtWidgets.QWidget.__init__(self, parent)



if __name__ == "__main__":
    monitors_resolution = []
    def monitors_info():
            for i, monitor_data in enumerate(get_monitors()):
                splited = str(monitor_data).split(',')
                monitor = [str(splited[-1].split('DISPLAY')[-1].split("'")[0]),
                           str(splited[-3].split('=')[-1]),
                           str(splited[-2].split('=')[-1])]
                            
                monitors_resolution.append(monitor)

    monitors_info()
    print(monitors_resolution)

    app = QtWidgets.QApplication(sys.argv)

    instance = MainWindow(monitor_number=monitors_resolution[0][0], #ScreenshotWidget
                          screen_width=monitors_resolution[0][1], 
                          screen_height=monitors_resolution[0][2])

    # instance.show()
    sys.exit(app.exec_()) 
