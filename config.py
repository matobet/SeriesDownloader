RSS_URL = 'http://www.rlslog.net/category/tv-shows/feed/'
SETTINGS_FILE = 'settings.cfg'

from PyQt4.QtCore import *
from PyQt4.QtGui import *



DEFAULT_WATCHED_SHOWS = ['House',                  
                         'The Big Bang Theory',                  
                         'South Park',                  
                         'Fringe',                  
                         'How I Met Your Mother',                  
                         'Dexter',                  
                         'Chuck',                  
                         'Family Guy',                 
                         'American Dad',              
                         'Futurama']

def save(shows):
    try:
        open(SETTINGS_FILE, 'w').write('\n'.join(map(str, shows)))
    except IOError:
        QMessageBox.critical(None, "Fata Error", "Error on writing the settings file")
        
def load():
    try:
        return [line.strip() for line in open(SETTINGS_FILE).readlines()]
    except IOError:
        return DEFAULT_WATCHED_SHOWS