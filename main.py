import sys
import random
import time
import numpy as np
from PIL import ImageQt

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

import make_screenshot


class Main_Menu(QtWidgets.QMainWindow):
    DELAY_TIMES = ['None', '1s', '2s', '3s', '4s', '5s', '10s']

    def __init__(self, snipped_pic=None):
        super().__init__()
        self.snipped_pic = snipped_pic

    def pass_instance(self, m_instance):
        self.m_instance = m_instance
        self.UI()

    def UI(self):   
        self.new_snip_button = QPushButton('new', self)
        self.new_snip_button.move(0, 0)
        self.new_snip_button.clicked.connect(self.new_snipping_windows)

        self.delay_combo = QComboBox(self)
        self.delay_combo.addItems(Main_Menu.DELAY_TIMES)
        self.delay_combo.move(120, 0)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setWindowTitle('snippus')
        self.resize(300, 200)
        self.show()

    def make_shots(self):
        self.monitors_data = []

        display = Gdk.Display.get_default()
        num_monitors = display.get_n_monitors()

        for i in range(0, num_monitors):
            monitor = display.get_monitor(i)
            monitor_rect = monitor.get_geometry()

            window = Gdk.get_default_root_window()
            self.picture = Gdk.pixbuf_get_from_window(window, 
                                monitor_rect.x, monitor_rect.y, 
                                monitor_rect.width, monitor_rect.height)

            self.monitors_data.extend([[self.picture, monitor_rect.width, monitor_rect.height, monitor_rect.x]])

        return self.monitors_data

    def new_snipping_windows(self):
        self.background_instances = []  
        self.mask_instances =[]
        self.close()
        if self.delay_combo.currentText() == 'None':
            time.sleep(0.3)
        else:   
            time.sleep(int(self.delay_combo.currentText()[:-1]))

        self.monitors_data = self.make_shots()

        for i, self.monitor_data in enumerate(self.monitors_data):
            self.background_instances.append(make_screenshot.BackgroundPicture(monitor_number=i,
                                                            picture=self.monitor_data[0],
                                                            screen_width=self.monitor_data[1], 
                                                            screen_height=self.monitor_data[2],
                                                            x_move=self.monitor_data[3]))

            self.mask_instances.append(make_screenshot.TransparentMask(monitor_number=i, 
                                                                    screen_width=self.monitor_data[1], 
                                                                    screen_height=self.monitor_data[2], 
                                                                    x_move=self.monitor_data[3]))

        [self.mask_instances[i].pass_instances(self.mask_instances, self.background_instances) 
                                       for i, _
                                       in enumerate(self.monitors_data)]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Main_Menu()
    widget.pass_instance(widget)
    # widget.show()
    sys.exit(app.exec_())