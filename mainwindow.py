from ui_mainwindow import Ui_MainWindow

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import config
from addshowdialog import AddShowDialog

import urllib2    
from lxml import etree
import re
import webbrowser

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.connect_slots()
        self.shows = config.load()
        self.listWidget.setSortingEnabled(True)
        self.updateListWidget()

    def connect_slots(self):
        self.addAction(self.actionAddShow)
        self.addAction(self.actionRemoveShow)
        
        self.btnCheck.clicked.connect(self.check)
        
        self.actionAddShow.triggered.connect(self.add_show)
        self.btnAdd.clicked.connect(self.add_show)
        
        self.actionRemoveShow.triggered.connect(self.remove_show)
                
    def add_show(self):
        dlg = AddShowDialog(self)
        dlg.exec_()
        if dlg.result() == QDialog.Accepted:
            show = dlg.show_name
            if show in self.shows: return 
            self.shows.append(show)
            self.updateListWidget()
            config.save(self.shows)
        
    def remove_show(self):
        item = self.listWidget.currentItem()
        if item is None: return
        self.shows.remove(item.text())
        self.updateListWidget()
        config.save(self.shows)
        
    def updateListWidget(self):
        self.listWidget.clear()
        self.listWidget.addItems(self.shows)
        
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.instance().exit()
            
        return QMainWindow.keyReleaseEvent(self, event)
    
    def check(self):
      
        response = urllib2.urlopen(config.RSS_URL)    
        xml = etree.parse(response)    
        items  = xml.findall('/channel/item')     
        news = []
        for item in items:        
            title = item.findtext('title')        
            if not self.watched(title): continue        
            content = item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')        
            try:            
                downloadLinks = [match[0] for match in re.findall(r'<a href="(http://www.(fileserve|filesonic|wupload).com/[^"]+)">', content)]            
                webbrowser.open(downloadLinks[0])
                news.append(title)        
            except IndexError:            
                pass

        message = "There are no new shows today for you :-(" if len(news) == 0 else \
            'These shows aired today:\n\n' + '\n'.join(news) + '\n\nYou will find links to them already opened in your browser.'
        QMessageBox.information(self, "Series Check", message) 

    def watched(self, title):    
        for show in self.shows:       
            if title.startswith(show):            
                return True    
        return False