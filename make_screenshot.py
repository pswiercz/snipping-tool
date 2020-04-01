from __future__ import print_function, unicode_literals, absolute_import
import numpy as np
import sys
import cv2
# import PIL
from PIL import ImageQt, ImageFilter, ImageEnhance
# from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtCore import Qt

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from gi.repository import GLib, GdkPixbuf
from PIL import Image

# import main

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

class TransparentMask(QtWidgets.QWidget):
    def __init__(self, monitor_number=None, screen_width=None, screen_height=None, x_move=None):
        super().__init__()
        
        self.monitor_number = int(monitor_number)
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)
        self.x_move = int(x_move)

    def pass_instances(self, mask_instances, background_instances):
        self.mask_instances = mask_instances
        self.background_instances = background_instances
        self.starter()

    def starter(self):
        self.setGeometry(self.x_move, 0, self.screen_width, self.screen_height)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #no title bar

        self.showFullScreen()
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.2)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def close_all(self):
        if isinstance(self.mask_instances, list):
            for for_closing in zip(self.mask_instances, self.background_instances):
                for_closing[0].close()
                for_closing[1].close()
        else:
            self.mask_instances.close()
            self.background_instances.close()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor("#000000"))
        # qp.setBrush(QtGui.QColor.fromHslF(0.9, 0.1, 0.8, 0.2))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.close_all()
        # TODO create new instance with main, pass already snipped picture 

class PictureBackground(QtWidgets.QMainWindow):
    def __init__(self, parent=None, monitor_number=None, picture=None, screen_width=None, screen_height=None, x_move=None):
        super().__init__(parent)

        self.monitor_number = int(monitor_number)
        self.picture = pixbuf2image(picture)
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)
        self.x_move = int(x_move)

        self.setGeometry(self.x_move, 0, self.screen_width, self.screen_height)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #no title bar
        self.showFullScreen()

        self.qimage = ImageQt.ImageQt(self.picture)
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap.fromImage(self.qimage)
        label.setPixmap(pixmap)
        self.setCentralWidget(label)

        self.show()

if __name__ == "__main__":
    monitor_data = []

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

    instance = PictureBackground(monitor_number=0,
                          picture=monitor_data[0],
                          screen_width=monitor_data[1], 
                          screen_height=monitor_data[2],
                          x_move=monitor_data[3])
   


    app_mask = QtWidgets.QApplication(sys.argv)
    mask_instance = TransparentMask(monitor_number=0,
                          screen_width=monitor_data[1], 
                          screen_height=monitor_data[2],
                          x_move=monitor_data[3])

    mask_instance.pass_instances(mask_instance, instance)

    # instance.show()

    # app_mask.aboutToQuit.connect(app_mask.deleteLater)
    # app.aboutToQuit.connect(app.deleteLater)
    app_mask.exit(app_mask.exec_()) 
    sys.exit(app.exec_()) 