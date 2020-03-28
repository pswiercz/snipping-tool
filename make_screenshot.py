from __future__ import print_function, unicode_literals, absolute_import
import numpy as np
import sys
import cv2
# import PIL
from PIL import ImageQt, ImageFilter, ImageEnhance
# from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtCore import Qt
# from screeninfo import get_monitors
# import main 
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from gi.repository import GLib, GdkPixbuf
from PIL import Image


def pixbuf2image(pix):
        data = pix.get_pixels()
        w = pix.props.width
        h = pix.props.height
        stride = pix.props.rowstride
        mode = "RGB"
        if pix.props.has_alpha == True:
            mode = "RGBA"
        im = Image.frombytes(mode, (w, h), data, "raw", mode, stride)
        return im

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, monitor_number=None, picture=None, screen_width=None, screen_height=None, x_move=None):
        # TODO Change monitor variables to *args, maybe
        super().__init__(parent)

        self.monitor_number = int(monitor_number)
        self.picture = pixbuf2image(picture)
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)
        self.x_move = int(x_move)

        self.starter()

    def starter(self):
        self.setGeometry(self.x_move, 0, self.screen_width, self.screen_height)
        self.begin = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #no title bar
        # self.setWindowOpacity(0.3) window transparency

        self.showFullScreen()

        # self.picture = self.picture.point(lambda p: p * 0.9)
        # # ImageFilter.GaussianBlur(radius=2) 
        # self.picture = self.picture.filter(ImageFilter.GaussianBlur(radius=1))
        # enhancer = ImageEnhance.Contrast(self.picture)
        # self.picture = enhancer.enhance(4.0)

        self.qimage = ImageQt.ImageQt(self.picture)

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
        # print(self.start)
        # self.end = self.start
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        # print(self.end)
        self.update()

# class Screenshot_tool(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         QtWidgets.QWidget.__init__(self, parent)



if __name__ == "__main__":
    monitor_data = []
    shots = []

    app = QtWidgets.QApplication(sys.argv)

    display = Gdk.Display.get_default()
    num_monitors = display.get_n_monitors()

    monitor = display.get_monitor(0)
    monitor_rect = monitor.get_geometry()

    window = Gdk.get_default_root_window()
    picture = Gdk.pixbuf_get_from_window(window, 
                        monitor_rect.x, monitor_rect.y, 
                        monitor_rect.width, monitor_rect.height)

    monitor_data.extend([picture, monitor_rect.width, monitor_rect.height, monitor_rect.x])

    instance = MainWindow(monitor_number=0, #ScreenshotWidget
                          picture=monitor_data[0],
                          screen_width=monitor_data[1], 
                          screen_height=monitor_data[2],
                          x_move=monitor_data[3])
   
    sys.exit(app.exec_()) 
