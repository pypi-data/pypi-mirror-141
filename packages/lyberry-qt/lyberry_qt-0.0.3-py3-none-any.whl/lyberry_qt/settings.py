import subprocess
import json
import appdirs
import os
import shutil

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from lyberry_qt.helpers import relative_path

this_dir = os.path.dirname(__file__)
default_conf = os.path.join(this_dir, 'conf.json')
conf_dir = appdirs.user_config_dir('lyberry')
conf_file_path = os.path.join(conf_dir, 'conf.json')
settings = {}

def load():
    try:
        conf_data = get_conf_data()
    except FileNotFoundError:
        try:
            shutil.copyfile(default_conf, conf_file_path)
        except FileNotFoundError:
            os.makedirs(conf_dir)
            shutil.copyfile(default_conf, conf_file_path)
        conf_data = get_conf_data()
    global settings
    settings = json.loads(conf_data)

def get_conf_data():
    with open(conf_file_path, 'r') as conf_file:
        return conf_file.read()

def apply():
    global settings
    with open(conf_file_path, 'w') as conf_file:
        conf_file.write(json.dumps(settings))

load()

def media_player(file):
    run_cmd(settings["player_cmd"], file)

def text_viewer(file):
    run_cmd(settings["viewer_cmd"], file)

def run_cmd(cmd, arg):
    command = cmd.split()
    try:
        i = command.index('{}')
        command.insert(i, arg)
        command.remove('{}')
    except:
        command.append(arg)
    subprocess.run(command)

class SettingsScreen(QtWidgets.QDialog):
    def __init__(self):
        super(SettingsScreen, self).__init__()
        loadUi(relative_path('designer/settings.ui'), self)
        
        self.row = 0
        self.inputs = []
        self.labels = []
        for key in settings:
            self.add_input(key, settings[key])

        self.apply_button.clicked.connect(self.done)

    def done(self, something_else):
        apply()
        self.close()
    
    def add_input(self, key, value):
        label = QtWidgets.QLabel()
        label.setText(key)
        self.formLayout.setWidget(self.row, QtWidgets.QFormLayout.LabelRole, label)
        self.labels.append(label)

        lineEdit = QtWidgets.QLineEdit()
        lineEdit.setText(value)
        self.formLayout.setWidget(self.row, QtWidgets.QFormLayout.FieldRole, lineEdit)
        def idk():
            settings[label.text()] = lineEdit.text()
        lineEdit.editingFinished.connect(idk)
        self.inputs.append(lineEdit)

        self.row += 1

class AccountsScreen(QtWidgets.QDialog):
    def __init__(self, lbry):
        super(AccountsScreen, self).__init__()
        loadUi(relative_path('designer/account.ui'), self)
        self._lbry = lbry
        for account in self._lbry.accounts:
            self._add_account_to_list(account)

        self.add_acc_button.clicked.connect(lambda: self.add_account())

    def add_account(self):
        try:
            account = self._lbry.add_account(
                self.edit_name.text(),
                self.edit_priv_key.text())
        except ValueError:
            print('invalid key!')
            return

        self._add_account_to_list(account)

    def _add_account_to_list(self, account):
        label = QtWidgets.QLabel()
        label.setText(account_to_html(account))
        self.acc_list_section.addWidget(label)
        if not account.is_default:
            default_button = QtWidgets.QPushButton()
            default_button.clicked.connect(account.set_as_default)
            default_button.setText(f'Set {account.name} as the default account')
            self.acc_list_section.addWidget(default_button)

            remove_button = QtWidgets.QPushButton()
            remove_button.clicked.connect(lambda: account.remove())
            remove_button.setText(f'Remove {account.name}')
            self.acc_list_section.addWidget(remove_button)

def account_to_html(account):
    return f'''
<h2>{account.name}{" - Default" if account.is_default else ""}</h2>
<p>
id: {account.id}
<br>
public key: {account.public_key}
</p>
'''
