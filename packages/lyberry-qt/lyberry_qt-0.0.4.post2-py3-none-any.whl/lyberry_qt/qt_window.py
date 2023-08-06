from PyQt5 import QtWidgets, uic

import lyberry_api.pub as lbry_pub
import lyberry_api.channel as lbry_channel
from lyberry_qt import settings, helpers
from lyberry_qt.following_screen import FollowingScreen, ChannelScreen
from lyberry_qt.connect import ConnectingWidget
from lyberry_qt.pub_screen import PubScreen

import re

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, lbry):
        super(MainWindow, self).__init__()
        uic.loadUi(helpers.relative_path('designer/main.ui'), self)
        self.following_button.clicked.connect(self.following_screen)

        self.settings_screen = settings.SettingsScreen()
        self.settings_button.clicked.connect(lambda: self.show_settings_screen())

        self.back_button.clicked.connect(self.go_back)
        self.go_button.clicked.connect(self.go_to_url)
        self.url_line_edit.returnPressed.connect(self.go_to_url)

        self._lbry = lbry

        if not self._lbry.online():
            self.settings_screen.account_button.setEnabled(False)
            connecting_window = ConnectingWidget(self._lbry)
            self.show_screen(connecting_window)
            connecting_window.finished.connect(self.when_connected)
        else:
            self.when_connected()


    def when_connected(self):
        self.accounts_screen = settings.AccountsScreen(self._lbry)
        self.settings_screen.account_button.setEnabled(True)
        self.settings_screen.account_button.clicked.connect(lambda: self.show_screen(self.accounts_screen))
        self.following_screen()

    def following_screen(self):
        try:
            following = FollowingScreen(self, self._lbry.sub_feed)
            self.show_screen(following)
        except ConnectionError:
            self.show_connecting_screen()
    
    def show_connecting_screen(self):
        self.show_screen(ConnectingWidget(self._lbry))
    
    def show_settings_screen(self):
        self.show_screen(self.settings_screen)

    def go_to_url(self):
        url = self.url_line_edit.text().strip()
        url = re.sub(r'^(https?://)?odysee.com/', 'lbry://', url)
        if url.startswith('lbry://') or url.startswith('@'):
            self.go_to_lbry_url(url)
        elif url.startswith('about:'):
            page = url.split(':')[1]
            if page in ['following', 'feed', 'subs', 'subscriptions']:
                self.following_screen()
    
    def go_to_lbry_url(self, url):
            claim = self._lbry.resolve(url)
            if type(claim) is lbry_pub.LBRY_Pub:
                self.show_pub(claim)
            elif type(claim) is lbry_channel.LBRY_Channel:
                self.show_channel(claim)
            else:
                print(type(claim))

    def show_channel(self, claim):
        channel_screen = ChannelScreen(self, claim)
        self.show_screen(channel_screen)
        self.url_line_edit.setText(claim.url)

    def show_pub(self, claim):
        pub_screen = PubScreen(self, claim)
        self.show_screen(pub_screen)
        self.url_line_edit.setText(claim.url)

    def show_screen(self, screen):
        self.stackedWidget.addWidget(screen)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        screen.finished.connect(lambda: self.stackedWidget.removeWidget(screen))
    
    def go_back(self):
        self.stackedWidget.currentWidget().close()


