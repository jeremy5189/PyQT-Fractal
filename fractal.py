import sys
import signal
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QEvent

class MainWindow(QWidget):
    
    def __init__(self, args):
        
        super(self.__class__, self).__init__()

        print('-- args --')
        print(args)
        
        self.setMouseTracking(True)
        self.installEventFilter(self)

        # Init recur time
        self.limit = 1

        if len(args) < 2:
            exit(0)
        
        if args[1] != None and args[1] == '1':

            # 3/4/5
            self.cos_theta   = 4 / 5;
            self.sin_theta   = 3 / 5;

        else:

            # 5/12/13
            self.cos_theta   = 12 / 13;
            self.sin_theta   = 5 / 13;

        self.theta_left  = math.acos(self.sin_theta) * 180 / math.pi
        self.theta_right = math.acos(self.sin_theta) * 180 / math.pi
        
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
        
            # Color
            c = n * 24
            if c > 255:
                c = 255

            color = QColor(255, c, c)
            pen   = QPen(color)
            pen.setWidth(2)
            painter.setPen(pen)
            rect_left = QRectF(x, y, r, r)
            painter.fillRect(rect_left, QBrush(color))
            painter.drawRects(rect_left)
            
            left_x = x
            left_y = y - r * self.cos_theta
            left_r =     r * self.cos_theta

            right_x = (r - r * self.sin_theta) + x
            right_y =  y - r * self.sin_theta
            right_r =      r * self.sin_theta

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
            elif event.button() == Qt.RightButton:
                self.limit -= 1
        
            self.repaint()

        return super(self.__class__, self).eventFilter(source, event)

if __name__ == "__main__":

    # Ctrl + C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    MainWindow = MainWindow(sys.argv)
    sys.exit(app.exec_())