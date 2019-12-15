import sys
import random
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import make_screenshot
from screeninfo import get_monitors


class Main_Menu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.monitors_info()
        self.UI()


    def UI(self):   
        self.layout = QtWidgets.QVBoxLayout()

        self.new_snip = QtWidgets.QPushButton("New") 
        self.new_snip.clicked.connect(self.new_snipping_window)

        self.delay_list = ['None', '1s', '2s', '3s', '4s', '5s', '10s']
        self.delay_combo = QComboBox(self)
        self.delay_combo.addItems(self.delay_list)

        self.layout.addWidget(self.new_snip, 1)
        self.layout.addWidget(self.delay_combo, 0)

        self.setLayout(self.layout)

    def monitors_info(self):
        self.monitors_resolution = []
        for i, monitor_data in enumerate(get_monitors()):
            splited = str(monitor_data).split(',')
            monitor = [str(splited[-1].split('DISPLAY')[-1].split("'")[0]),
                       str(splited[-3].split('=')[-1]),
                       str(splited[-2].split('=')[-1])]
                        
            self.monitors_resolution.append(monitor)

    def new_snipping_window(self):
        self.close()
        if self.delay_combo.currentText() != 'None':
            time.sleep(int(self.delay_combo.currentText()[:-1]))
        

        # TODO: place to take printscreen
        from desktopmagic.screengrab_win32 import getDisplaysAsImages

        # print(self.monitors_resolution)
        
        self.make_screenshot_instance = []
        [self.make_screenshot_instance.append(make_screenshot.MainWindow(monitor_number=self.monitors_resolution[i][0], #ScreenshotWidget
                                                                         screen_width=self.monitors_resolution[i][1], 
                                                                         screen_height=self.monitors_resolution[i][2])) 
                                                                         for i, monitor in enumerate(self.monitors_resolution)]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Main_Menu()
    widget.resize(300, 200)
    widget.show()

    sys.exit(app.exec_())