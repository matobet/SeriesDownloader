from ui_mainwindow import Ui_MainWindow

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import config
from addshowdialog import AddShowDialog

import urllib2    
from lxml import etree
import re
import webbrowser

WATCHED_SHOWS = ['House',                  
                 'The Big Bang Theory',                  
                 'South Park',                  
                 'Fringe',                  
                 'How I Met Your Mother',                  
                 'Dexter',                  
                 'Chuck',                  
                 'Family Guy',                 
                 'American Dad',              
                 'Futurama']

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.btnCheck.clicked.connect(self.check)
        self.actionAddShow.triggered.connect(self.addShow)
        self.addAction(self.actionAddShow)
        self.btnAdd.clicked.connect(self.addShow)
        self.addAction(self.actionRemoveShow)
        self.actionRemoveShow.triggered.connect(self.removeShow)
        self.listWidget.setSortingEnabled(True)
        self.shows = config.load()
        self.updateListWidget()
        
    def addShow(self):
        dlg = AddShowDialog(self)
        dlg.exec_()
        if dlg.result() == QDialog.Accepted:
            show = dlg.show_name
            if show in self.shows: return 
            self.shows.append(show)
            self.updateListWidget()
            config.save(self.shows)
        
    def removeShow(self):
        show = self.listWidget.currentItem().text()
        self.shows.remove(show)
        self.updateListWidget()
        config.save(self.shows)
        
    def updateListWidget(self):
        self.listWidget.clear()
        self.listWidget.addItems(self.shows)
    
    def check(self):
      
        response = urllib2.urlopen(config.RSS_URL)    
        xml = etree.parse(response)    
        items  = xml.findall('/channel/item')     
        for item in items:        
            title = item.findtext('title')        
            if not self.watched(title): continue        
            content = item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')        
            print(title)        
            try:            
                downloadLinks = [match[0] for match in re.findall(r'<a href="(http://www.(fileserve|filesonic|wupload).com/[^"]+)">', content)]            
                webbrowser.open(downloadLinks[0])        
            except IndexError:            
                pass

        QMessageBox.information(self, "hello", "Checked") 

    def watched(self, title):    
        for show in self.shows:       
            if title.startswith(show):            
                return True    
        return False