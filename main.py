import sys
import random
import time
import numpy as np
from PIL.ImageQt import ImageQt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import make_screenshot
from screeninfo import get_monitors

from desktopmagic.screengrab_win32 import getDisplaysAsImages


class Main_Menu(QtWidgets.QWidget):
    DELAY_TIMES = ['None', '1s', '2s', '3s', '4s', '5s', '10s']
    INSTANCES = []
    def __init__(self):
        super().__init__()
        self.monitors_info()
        self.UI()

    def UI(self):   
        self.layout = QtWidgets.QVBoxLayout()

        self.new_snip = QtWidgets.QPushButton("New") 
        self.new_snip.clicked.connect(self.new_snipping_windows)

        self.delay_combo = QComboBox(self)
        self.delay_combo.addItems(Main_Menu.DELAY_TIMES)

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

    def new_snipping_windows(self):
        # self.close()

        if self.delay_combo.currentText() == 'None':
            time.sleep(0.3)
            # print("none")
        else:
            time.sleep(int(self.delay_combo.currentText()[:-1]))
        

        # TODO: place to take printscreen
        self.shots = []
        for displayNumber, im in enumerate(getDisplaysAsImages(), 1):
            # im.save(f'picures/_{displayNumber}.png', format='png')
            # im.show()
            # self.qim = ImageQt(im)
            # self.shots.append(self.qim)
            self.shots.append(im)
            # print(im)
            # if displayNumber == 1:
            #     break
        # print(self.shots)
        # pictures[0].show()

        [Main_Menu.INSTANCES.append(make_screenshot.MainWindow(
                                    monitor_number=self.monitors_resolution[i][0], #ScreenshotWidget
                                    screen_width=self.monitors_resolution[i][1], 
                                    screen_height=self.monitors_resolution[i][2],
                                    shot=self.shots[i]),)
                                    for i, monitor in enumerate(self.monitors_resolution)]
        # print(Main_Menu.INSTANCES)

        # self.close() #test

        # self.make_screenshot_instance = []
        # [self.make_screenshot_instance.append(make_screenshot.MainWindow(
        #                             monitor_number=self.monitors_resolution[i][0], #ScreenshotWidget
        #                             screen_width=self.monitors_resolution[i][1], 
        #                             screen_height=self.monitors_resolution[i][2],
        #                             shot=self.shots[i]),)
        #                             for i, monitor in enumerate(self.monitors_resolution)]
        # print(self.make_screenshot_instance)

        # self.monitor = 0
        # self.make_screenshot_instance.append(make_screenshot.MainWindow(
        #                             monitor_number=self.monitors_resolution[self.monitor][0], #ScreenshotWidget
        #                             screen_width=self.monitors_resolution[self.monitor][1], 
        #                             screen_height=self.monitors_resolution[self.monitor][2],
        #                             shot=self.shots[self.monitor]))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    widget = Main_Menu()
    widget.resize(300, 200)
    widget.show()
    print(widget.INSTANCES)

    sys.exit(app.exec_())