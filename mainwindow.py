from ui_mainwindow import Ui_MainWindow

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import config

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
                 'American Dad'              
                 'Futurama']

def watched(title):    
    for show in WATCHED_SHOWS:       
        if title.startswith(show):            
            return True    
    return False

def doStuff():    
      
    response = urllib2.urlopen(config.RSS_URL)    
    xml = etree.parse(response)    
    items  = xml.findall('/channel/item')     
    for item in items:        
        title = item.findtext('title')        
        if not watched(title): continue        
        content = item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded')        
        print(title)        
        try:            
            downloadLinks = [match[0] for match in re.findall(r'<a href="(http://www.(fileserve|filesonic|wupload).com/[^"]+)">', content)]            
            webbrowser.open(downloadLinks[0])        
        except IndexError:            
            pass

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
        
    def addShow(self):
        QMessageBox.information(self, "hello", "Add Show")
        
    def removeShow(self):
        QMessageBox.information(self, "hello", "remove show")
    
    def check(self):
        doStuff()
        QMessageBox.information(self, "hello", "Checked")