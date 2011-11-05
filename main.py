from mainwindow import MainWindow

from PyQt4.QtGui import *
import sys
import config

if __name__ == '__main__':  
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())