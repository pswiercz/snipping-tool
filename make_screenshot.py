import numpy as np
import sys
import cv2
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from screeninfo import get_monitors

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, monitor_number=None, screen_width=None, screen_height=None):
        # TODO Change monitor variables to *args
        super().__init__(parent)
        QtWidgets.QMainWindow.__init__(self, parent)

        self.monitor_number = int(monitor_number) - 1 #Qt is starting reading screen number from 0
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)

        
        self.screenshot_tool_widget = Screenshot_tool(parent=self)
        self.setCentralWidget(self.screenshot_tool_widget)

        # self.QMenu.setTitle('sdawdawdawd')

        self.starter()

    def starter(self):
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        # self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowOpacity(0.3) window transparency

        self.monitor = QtWidgets.QDesktopWidget().screenGeometry(self.monitor_number)
        self.move(self.monitor.left(), self.monitor.top())

        # self.QMenu.setWindowTitle('asd')
        self.show()

class Screenshot_tool(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        QtWidgets.QWidget.__init__(self, parent)



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
