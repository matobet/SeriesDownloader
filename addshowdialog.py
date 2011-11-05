'''
Created on Nov 5, 2011

@author: matobet
'''

from PyQt4.QtGui import *
from ui_addshowdialog import Ui_Dialog

class AddShowDialog(QDialog, Ui_Dialog):
    
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setupUi(self)
        
    @property
    def show_name(self):
        return self.lineEdit.text()