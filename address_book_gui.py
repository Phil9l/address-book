#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Apr 26 00:14:44 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

import sys
import threading
import json
import time
from address_book import AddressBook
from PyQt5 import QtCore, QtGui, QtWidgets
from friends import VK_Friend, Twitter_Friend, Friend
from utils import VK_API, Twitter_API



class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(470, 490)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralWidget)
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 411, 428))
        self.gridLayout_4 = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents)
        self.gridLayout_2 = QtWidgets.QGridLayout()

        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_3.addWidget(self.progressBar, 1, 0, 1, 1)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralWidget)
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addWidget(self.pushButton_1)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self._set_status_message()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _set_status_message(self, message="Doing nothing"):
        self.statusBar.showMessage(message)

    def _set_progress(self, percentage):
        self.progressBar.setValue(percentage)

    @staticmethod
    def _disable_button(button):
        button.setEnabled(False)
        button.setDisabled(True)

    @staticmethod
    def _enable_button(button):
        button.setEnabled(True)
        button.setDisabled(False)

    def _lock_buttons(self, message):
        self.progressBar.setValue(0)
        self._set_status_message(message)
        self._disable_button(self.pushButton)
        self._disable_button(self.pushButton_1)
        self._disable_button(self.pushButton_2)

    def _unlock_buttons(self):
        self.progressBar.setValue(0)
        self._set_status_message()
        self._enable_button(self.pushButton)
        self._enable_button(self.pushButton_1)
        self._enable_button(self.pushButton_2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.comboBox.setItemText(0, _translate("MainWindow", "VK"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Twitter"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "user id"))
        self.pushButton.setText(_translate("MainWindow", "Add Friends"))
        self.pushButton_1.setText(_translate("MainWindow", "Merge"))
        self.pushButton_2.setText(_translate("MainWindow", "Save Contacts"))

    def add_row(self, row_index, parent, title_text, value_text):
        _translate = QtCore.QCoreApplication.translate
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        value_field = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        parent.addWidget(value_field, row_index, 1, 1, 1)
        title_field = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        title_field.setFont(font)
        parent.addWidget(title_field, row_index, 0, 1, 1)

        value_field.setText(_translate("MainWindow", value_text))
        title_field.setText(_translate("MainWindow", title_text))

    def add_item(self, item_id, title_text, fields):
        UserItem = QtWidgets.QGridLayout()
        Title = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        Title.setFont(font)
        UserItem.addWidget(Title, 0, 0, 1, 1)
        information = QtWidgets.QGridLayout()
        UserItem.addLayout(information, 1, 0, 1, 1)

        line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.gridLayout_2.addLayout(UserItem, 2 * item_id, 0, 1, 1)
        self.gridLayout_2.addWidget(line, 2 * item_id + 1, 0, 1, 1)

        for index, field in enumerate(fields):
            self.add_row(index, information, field[0], field[1])

        _translate = QtCore.QCoreApplication.translate
        Title.setText(_translate("MainWindow", title_text))


class MyApp(Ui_MainWindow, QtWidgets.QMainWindow, AddressBook):
    def __init__(self, title_field, fields, parent=None, name=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)

        self.title_field = title_field
        self.fields = fields
        self.friend_list = []

        self.comm = Communicate()
        self.comm.signal.connect(self._handle_data)

        self.pushButton.clicked.connect(self.add_friends)
        self.pushButton_1.clicked.connect(self.merge_friend_list)
        self.pushButton_2.clicked.connect(self.save_CSV)

        self._gui_merge_result = None

        self.user_id = 0

    def _clear_layout(self, layout):
        self.user_id = 0
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QtWidgets.QWidgetItem):
                item.widget().setParent(None)
            elif isinstance(item, QtWidgets.QSpacerItem):
                pass
            else:
                self._clear_layout(item.layout())

    def _add_friends_to_gui(self, friends, comm):
        for index, friend in enumerate(friends):
            fields = []
            for field in self.fields:
                if hasattr(friend, field) and getattr(friend, field) != '':
                    fields.append((self.fields[field],
                                  str(getattr(friend, field))))
            data_dict = {'action': 'add_friend', 'fields': fields,
                         'title': getattr(friend, self.title_field)}
            comm.signal.emit(json.dumps(data_dict))

            progress = index * 100 // len(friends)
            comm.signal.emit(json.dumps({'action': 'set_progress',
                                         'progress': progress}))
            time.sleep(0.1)

    def add_friends_thread(self, comm):
        method = 'VK' if self.comboBox.currentIndex() == 0 else 'Twitter'
        label = "Getting {} friends information.".format(method)
        comm.signal.emit(json.dumps({'action': 'lock', 'label': label}))
        friends = self.get_friends()
        self.friend_list += friends
        self._add_friends_to_gui(friends, comm)
        comm.signal.emit(json.dumps({'action': 'unlock'}))

    def merge_friends_thread(self, comm):
        comm.signal.emit(json.dumps({'action': 'lock',
                                     'label': 'Merging friends'}))
        comm.signal.emit(json.dumps({'action': 'clear_layout'}))
        set_percentage = lambda x: comm.signal.emit(json.dumps(
            {'action': 'set_progress', 'progress': x}))
        self.friend_list = self._merge_friend_lists(self.friend_list,
                                                    set_percentage)

        comm.signal.emit(json.dumps({'action': 'lock',
                                     'label': 'Saving merged friends'}))
        self._add_friends_to_gui(self.friend_list, comm)
        comm.signal.emit(json.dumps({'action': 'unlock'}))

    def get_friends(self):
        user_id = self.lineEdit.text()
        if self.comboBox.currentIndex() == 0:
            api = VK_API()
            friend_class = VK_Friend
        else:
            api = Twitter_API()
            friend_class = Twitter_Friend
        try:
            friend_list = [
                friend_class(**friend) for friend in api.get_friends(user_id)
            ]
            return friend_list
        except ValueError:
            self.comm.signal.emit(json.dumps({'action': 'error',
                                              'title': 'Wrong ID',
                                              'data': ('No user with such id '
                                                       'found.')}))
            return []

    @staticmethod
    def _show_question(question_text, additional_text, title,
                       buttons=None):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Question)
        msg_box.setText(question_text)
        msg_box.setInformativeText(additional_text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.No |
                                   QtWidgets.QMessageBox.Yes)
        if buttons is not None:
            first_button = msg_box.button(QtWidgets.QMessageBox.No)
            first_button.setText(buttons[0])
            second_button = msg_box.button(QtWidgets.QMessageBox.Yes)
            second_button.setText(buttons[1])
        retval = msg_box.exec_()
        return retval == QtWidgets.QMessageBox.Yes

    def _get_gui_merge_result(self):
        while self._gui_merge_result is None:
            time.sleep(0.01)
        result = self._gui_merge_result
        self._gui_merge_result = None
        return result

    def merge_friend_list(self):
        my_thread = threading.Thread(target=self.merge_friends_thread,
                                     args=(self.comm,))
        my_thread.start()

    def _merge_friends(self, friend1, friend2):
        question = ('{} and {} seem to be equal. Do you want to '
                    'merge them?').format(friend1.full_name, friend2.full_name)

        self.comm.signal.emit(json.dumps({'action': 'ask',
                                          'params': [question, '',
                                                     'Merge friends']}))
        need_merge = self._get_gui_merge_result()

        if not need_merge:
            return
        result = Friend(**vars(friend1))
        for attr in vars(friend1):
            if getattr(friend1, attr) != getattr(friend2, attr):
                if getattr(friend1, attr) == '':
                    setattr(result, attr, getattr(friend2, attr))
                elif getattr(friend2, attr) == '':
                    setattr(result, attr, getattr(friend1, attr))
                else:
                    question = 'Difference in {} field:'.format(
                        self.fields[attr])
                    extra_data = 'User1 value: {}\nUser2 value: {}'.format(
                        getattr(friend1, attr), getattr(friend2, attr))

                    params = [question, extra_data, 'Merge Friends',
                              ('First', 'Second')]
                    self.comm.signal.emit(json.dumps({'action': 'ask',
                                                      'params': params}))
                    res = self._get_gui_merge_result()
                    if res:
                        setattr(result, attr, getattr(friend2, attr))
        return result

    def _handle_data(self, data):
        data_dict = json.loads(data)
        if data_dict['action'] == 'lock':
            self._lock_buttons(data_dict['label'])
        elif data_dict['action'] == 'unlock':
            self._unlock_buttons()
        elif data_dict['action'] == 'clear_layout':
            self._clear_layout(self.gridLayout_2)
        elif data_dict['action'] == 'ask':
            self._gui_merge_result = self._show_question(*data_dict['params'])
        elif data_dict['action'] == 'set_progress':
            progress = data_dict.get('progress', 0)
            self._set_progress(progress)
        elif data_dict['action'] == 'error':
            QtWidgets.QMessageBox.critical(self, data_dict['title'],
                                           data_dict['data'])
        else:
            fields = data_dict['fields']
            title = data_dict['title']
            self.user_id += 1
            self.add_item(self.user_id, title, fields)

    def add_friends(self):
        my_thread = threading.Thread(target=self.add_friends_thread,
                                     args=(self.comm,))
        my_thread.start()

    def save_CSV(self, filename=None):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Dialog Title',
                                                         'contacts.csv')
        if filename[0]:
            with open(filename[0], 'w') as out_file:
                out_file.write(self._generate_CSV(self.fields,
                                                  self.friend_list))
            QtWidgets.QMessageBox.information(self, 'Success', 'Statistics '
                                              'was saved successfully.')


if __name__ == "__main__":
    csv_fields = {
        'full_name': 'Name',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'bdate': 'Birthday',
        'phone': 'Mobile Phone',
        'email': 'E-mail Address',
    }
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp('full_name', csv_fields)
    window.show()
    sys.exit(app.exec_())
