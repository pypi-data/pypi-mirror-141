#!/usr/bin/env python3

import lyberry_api.api as lbry_api
import lyberry_api.pub as lbry_pub
import lyberry_api.channel as lbry_channel

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.uic import loadUi

from lyberry_qt.connect import ConnectingWidget
from lyberry_qt.helpers import relative_path

import sys
import os
import requests
import traceback
import time

from lyberry_qt import settings

app_settings = settings.settings

lbry = lbry_api.LBRY_Api(
        lbrynet_api = app_settings['lbrynet_api'],
        comment_api = app_settings['comment_api']
        )

IMAGE_DIR = './images/'

thumb_path = '/tmp/lyberry_thumbs/'
if not os.path.isdir(thumb_path):
    os.mkdir(thumb_path)

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
                window.show_screen(ConnectingWidget(lbry))
                break
            if next_item:
                items.append(next_item)
        self.finished.emit(items)

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
        except:
            self.default()
    
    def default(self):
        pixmap = QtGui.QPixmap()
        pixmap.load(IMAGE_DIR+'NotFound.png')
        self.finished.emit(pixmap)

class Loader(QObject):
    finished = pyqtSignal()
    def set_func(self, func):
        self.func = func
    def run(self):
        self.func()
        self.finished.emit()

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

class ListScreen(QtWidgets.QDialog):
    def __init__(self):
        super(ListScreen, self).__init__()
        loadUi(relative_path('designer/following.ui'), self)
        self.title_label.setText(self.title)
        self.load_more_button.clicked.connect(self.more)
        self.amt = 2
        self.width = 2
        self.items = []
        self.img_threads = [QThread() for i in range(4)]
        self.img_thread_no = 0
        self.thread = QThread()

    def new_pub(self, pub):
        item = PubWidget(pub, self.img_threads[self.img_thread_no])
        self.img_thread_no = (self.img_thread_no + 1) % len(self.img_threads)
        self.items.append(item)

        self.gridLayout.addWidget(item, self.amt // self.width, self.amt % self.width, 1, 1)
        self.amt += 1
        return item.pub_grid
    
    def pubs_to_list(self, pubs):
        for pub in pubs:
            self.new_pub(pub)
        self.gridLayout.addWidget(self.load_more_button, self.amt // self.width +1, 0, 1, 2)
        for thread in self.img_threads:
            thread.start()
        self.scrollArea.ensureWidgetVisible(self.load_more_button)

    def more(self):
        self.load_more_button.setEnabled(False)

        self.worker = FeedUpdater()
        self.worker.set_feed(self.feed)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.pubs_to_list)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()
        self.thread.finished.connect(
            lambda: self.load_more_button.setEnabled(True)
        )

    def view(self):
        window.show_screen(self)
        window.url_line_edit.setText(self.url)

class FollowingScreen(ListScreen):
    def __init__(self):
        self.feed = lbry.sub_feed
        self.title = 'Following'
        self.url = 'about:following'
        super(FollowingScreen, self).__init__()

class ChannelScreen(ListScreen):
    def __init__(self, channel):
        self.title = channel.name
        self.description = channel.description
        self.channel = channel
        self.feed = channel.pubs_feed
        self.url = channel.url
        super(ChannelScreen, self).__init__()
        markdown_to_label(self.description, self.description_label)
        self.follow_button.clicked.connect(self.channel.follow)

def markdown_to_label(markdown_text, label):
    # html_text = markdown.convert(markdown_text)
    html_text = markdown_text
    label.setText(html_text)
    label.setWordWrap(True)

class PubScreen(QtWidgets.QDialog):
    def __init__(self, pub):
        super(PubScreen, self).__init__()
        loadUi(relative_path('designer/pub.ui'), self)
        self.pub = pub
        self.title_label.setText(self.pub.title)

        markdown_to_label(self.pub.description, self.description_label)

        self.channel_button.setText(self.pub.channel.name)
        self.channel_button.clicked.connect(lambda: view_channel(self.pub.channel))

        self.amt = 1
        self.comments = []
        self.comments_button.clicked.connect(self.more_comments)

        self.open_thread = QThread()
        self.open_on(self.open_thread)
        self.open_button.clicked.connect(self.open_thread.start)

        self.comment_thread = QThread()
        self.add_my_channels_as_comment_options()
        self.create_comment_button.clicked.connect(self.create_comment)
    
    def open_on(self, play_thread):
        self.opener = Loader()
        self.opener.set_func(self.open)
        self.opener.moveToThread(play_thread)
        play_thread.started.connect(self.opener.run)

    def open(self):
        open_external(self.pub)
    
    def add_my_channels_as_comment_options(self):
        my_channels = lbry.my_channels
        for channel in my_channels:
            self.channel_select.addItem(channel.name)

    def create_comment(self):
        channel_name = self.channel_select.currentText()
        channel = lbry.channel_from_uri(channel_name)
        message = self.comment_box.toPlainText()
        lbry.make_comment(channel, message, self.pub)
        self.comment_box.clear()

    def show_comment(self, comment):
        item = CommentWidget(comment)
        self.comments.append(item)
        self.comments_section.addWidget(item, self.amt, 0, 1, 1)
        self.amt += 1
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    
    def list_comments(self, comments):
        for comment in comments:
            self.show_comment(comment)
        self.comments_section.addWidget(self.comments_button)
        self.scrollArea.ensureWidgetVisible(self.comments_button)

    def more_comments(self):
        self.comments_button.setEnabled(False)
        self.comment_worker = FeedUpdater()
        self.comment_worker.set_feed(self.pub.comments_feed)
        self.comment_worker.moveToThread(self.comment_thread)
        self.comment_thread.started.connect(self.comment_worker.run)
        self.comment_worker.finished.connect(self.list_comments)
        self.comment_worker.finished.connect(self.comment_worker.deleteLater)
        self.comment_worker.finished.connect(self.comment_thread.quit)
        self.comment_thread.finished.connect(
                lambda: self.comments_button.setEnabled(True)
        )
        self.comment_thread.start()
    
    def view(self):
        window.show_screen(self)
        window.url_line_edit.setText(self.pub.url)

class PubWidget(QtWidgets.QDialog):
    def __init__(self, pub, img_thread):
        super(PubWidget, self).__init__()
        loadUi(relative_path('designer/pub_thumb.ui'), self)
        self.loaders = []
        self.img_thread = img_thread
        self.pub = pub
        self.title.setText(pub.title)
        self.title.clicked.connect(self.view)
        self.img_url_to_label(pub.thumbnail, self.thumbnail)
        self.channel.setText(pub.channel.name)
        self.channel.clicked.connect(lambda: view_channel(self.pub.channel))

    def view(self):
        pub_screen = PubScreen(self.pub)
        pub_screen.view()

    def img_url_to_label(self, url, label):
        label.setText('Loading image')
        img_loader = ImageLoader()
        img_loader.set_url(url)
        self.loaders.append(img_loader)
        img_loader.moveToThread(self.img_thread)
        self.img_thread.started.connect(img_loader.run)
        img_loader.finished.connect(self.img_thread.quit)
        img_loader.finished.connect(img_loader.deleteLater)
        img_loader.finished.connect(label.setPixmap)

class CommentWidget(QtWidgets.QDialog):
    def __init__(self, comment):
        super(CommentWidget, self).__init__()
        loadUi(relative_path('designer/comment.ui'), self)
        self.comment = comment
        markdown_to_label(comment.msg, self.message)
        self.channel_button.setText(comment.channel.name)
        self.channel_button.clicked.connect(lambda: view_channel(comment.channel))
        self.show_replies_button.setText(str(comment.replies_amt) + " Replies")
        if comment.replies_amt > 0:
            self.show_replies_button.clicked.connect(self.show_replies)
        else:
            self.show_replies_button.setEnabled(False)
    
    def show_replies(self):
        for comment in self.comment.replies:
            item = CommentWidget(comment)
            self.replies_section.addWidget(item)
        self.show_replies_button.setEnabled(False)

def view_channel(channel):
    channel_screen = ChannelScreen(channel)
    channel_screen.view()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(relative_path('designer/main.ui'), self)
        self.following_button.clicked.connect(self.following_screen)

        self.settings_screen = settings.SettingsScreen()
        self.settings_button.clicked.connect(lambda: self.show_screen(self.settings_screen))

        self.back_button.clicked.connect(self.go_back)
        self.go_button.clicked.connect(self.go_to_url)
        self.url_line_edit.returnPressed.connect(self.go_to_url)

        if not lbry.online():
            self.settings_screen.account_button.setEnabled(False)
            connecting_window = ConnectingWidget(lbry)
            self.show_screen(connecting_window)
            connecting_window.finished.connect(self.when_connected)
        else:
            self.when_connected()


    def when_connected(self):
        self.accounts_screen = settings.AccountsScreen(lbry)
        self.settings_screen.account_button.setEnabled(True)
        self.settings_screen.account_button.clicked.connect(lambda: self.show_screen(self.accounts_screen))
        self.following_screen()

    def following_screen(self):
        try:
            following = FollowingScreen()
            self.show_screen(following)
        except ConnectionError:
            self.show_screen(ConnectingWidget(lbry))
    
    def go_to_url(self):
        url = self.url_line_edit.text()
        claim = lbry.resolve(url)
        if type(claim) is lbry_pub.LBRY_Pub:
            pub_screen = PubScreen(claim)
            pub_screen.view()
        elif type(claim) is lbry_channel.LBRY_Channel:
            channel_screen = ChannelScreen(claim)
            channel_screen.view()
        else:
            print(type(claim))

    def show_screen(self, screen):
        self.stackedWidget.addWidget(screen)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        screen.finished.connect(lambda: self.stackedWidget.removeWidget(screen))
    
    def go_back(self):
        self.stackedWidget.currentWidget().close()
        # self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

def open_external(pub):
    file_type = pub.media_type.split('/')[0]
    if file_type == 'video' or file_type == 'audio':
        settings.media_player(pub.streaming_url)
    elif file_type == 'text':
        settings.text_viewer(pub.streaming_url)

def main():
    app = QtWidgets.QApplication(sys.argv)
    start()
    sys.exit(app.exec_())

def start():
    global window
    window = MainWindow()
    window.show()

if __name__ == '__main__':
    main()
