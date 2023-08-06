
import os
import requests
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtGui

def relative_path(path):
    this_dir = os.path.dirname(__file__)
    return os.path.join(this_dir, path)

def markdown_to_label(markdown_text, label):
    label.setText(markdown_text)
    label.setWordWrap(True)

class FeedUpdater(QObject):
    finished = pyqtSignal(list)

    def set_feed(self, feed):
        self.feed = feed

    def run(self):
        items = []
        for i in range(20):
            try:
                next_item = next(self.feed)
            except StopIteration:
                break
            except KeyError:
                continue
            except ConnectionError:
                window.connecting_screen()
                break
            if next_item:
                items.append(next_item)
        self.finished.emit(items)

IMAGE_DIR = relative_path('./images/')

thumb_path = '/tmp/lyberry_thumbs/'
if not os.path.isdir(thumb_path):
    os.mkdir(thumb_path)

def download_file(url):
    local_filename = thumb_path+str(hash(url))
    if os.path.isfile(local_filename):
        return local_filename
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename


class ImageLoader(QObject):
    finished = pyqtSignal(QtGui.QPixmap)

    def set_url(self, url):
        self.url = url

    def run(self):
        pixmap = QtGui.QPixmap()
        try:
            file = download_file(self.url)
            pixmap.load(file)
            self.finished.emit(pixmap)
            return
        except Exception as err:
            print(f'Error loading image: {err}')
            self.default()
    
    def default(self):
        pixmap = QtGui.QPixmap()
        pixmap.load(IMAGE_DIR+'NotFound.png')
        self.finished.emit(pixmap)
