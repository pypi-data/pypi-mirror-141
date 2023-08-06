#!/usr/bin/env python3

import lyberry_api.api as lbry_api
import lyberry_api.pub as lbry_pub
import lyberry_api.channel as lbry_channel

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from lyberry_qt.helpers import relative_path

import sys
import os
import requests
import traceback
import time
import re

from lyberry_qt import settings
from lyberry_qt.qt_window import MainWindow

app_settings = settings.settings

lbry = lbry_api.LBRY_Api(
    lbrynet_api = app_settings['lbrynet_api'],
    comment_api = app_settings['comment_api']
)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(lbry)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
