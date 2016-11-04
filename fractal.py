import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QRectF, QEvent
import signal
import math


class MainWindow(QWidget):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.limit = 1
        self.theta_left = math.acos(3 / 5) * 180 / math.pi
        self.theta_right = math.acos(3 / 5) * 180 / math.pi
        
        # Starting Point
        self.x = 550
        self.y = 550
        self.r = 100
        self.initUI()


    def initUI(self):
        self.resize(1200, 800)
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.drawSquare(painter)
        painter.end()

    def drawSquare(self, painter):
        pen = QPen(Qt.blue)
        pen.setWidth(2)
        painter.setPen(pen)
        self.recurDraw(painter, 1, self.x, self.y, self.r)

    def turnLeft(self, painter, x, y):
        painter.translate(x, y)
        painter.rotate(360 - (90 - self.theta_left))
        painter.translate(-x, -y)

    def unTurnLeft(self, painter, x, y):
        painter.translate(x, y)
        painter.rotate(-(360 - (90 - self.theta_left)))
        painter.translate(-x, -y)

    def turnRight(self, painter, x, y, r):
        painter.translate(x + r, y)
        painter.rotate(self.theta_right)
        painter.translate(-(x + r), -y)

    def unTurnRight(self, painter, x, y, r):
        painter.translate(x + r, y)
        painter.rotate(-self.theta_right)
        painter.translate(-(x + r), -y)

    def recurDraw(self, painter, n, x, y, r):

        # Stop Recursive
        if n > self.limit:
            return

        else:
        
            rect_left = QRectF(x, y, r, r)
            painter.drawRects(rect_left)
            
            left_x = x
            left_y = y - r * 4/5
            left_r = r * 4/5

            right_x = (r - r * 3/5) + x
            right_y = y - r * 3 / 5
            right_r = r * 3 / 5

            # Draw Left
            self.turnLeft(painter, x, y)
            self.recurDraw(painter, n + 1, left_x, left_y, left_r)
            self.unTurnLeft(painter, x, y)

            # Draw Right
            self.turnRight(painter, x, y, r)
            self.recurDraw(painter, n + 1, right_x, right_y, right_r)
            self.unTurnRight(painter, x, y, r)


    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            
            # increase recursive level
            if event.button() == Qt.LeftButton:
                self.limit += 1
        
            self.repaint()

        return super(self.__class__, self).eventFilter(source, event)

if __name__ == "__main__":

    # Ctrl + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    sys.exit(app.exec_())
