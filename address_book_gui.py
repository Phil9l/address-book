#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import threading
import json
import time
from address_book import AddressBook
from Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from friends import VK_Friend, Twitter_Friend, Friend
from utils import VK_API, Twitter_API
from TwitterAPI import TwitterError


class Communicate(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)


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
        self._is_stopped = threading.Event()

        self.user_id = 0

    def _stopped(self):
        return self._is_stopped.isSet()

    def _stop(self):
        self._is_stopped.set()

    def _clear_layout(self, layout):
        self.user_id = 0
        for i in reversed(range(layout.count())):
            if self._stopped():
                break
            item = layout.itemAt(i)
            if isinstance(item, QtWidgets.QWidgetItem):
                item.widget().setParent(None)
            elif isinstance(item, QtWidgets.QSpacerItem):
                pass
            else:
                self._clear_layout(item.layout())

    def _add_friends_to_gui(self, friends, comm):
        for index, friend in enumerate(friends):
            if self._stopped():
                break
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

    def closeEvent(self, event):
        self._stop()

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

        def _set_percentage(x):
            comm.signal.emit(json.dumps({'action': 'set_progress',
                                         'progress': x}))

        self.friend_list = self._merge_friend_lists(self.friend_list,
                                                    _set_percentage,
                                                    self._stopped())

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
        except (ValueError, TwitterError.TwitterRequestError):
            self._wrong_id()
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

    def _wrong_id(self):
        self.comm.signal.emit(json.dumps({'action': 'error',
                                          'title': 'Wrong ID',
                                          'data': ('No user with such id '
                                                   'found.')}))

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
        my_thread.daemon = True
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
        'site': 'Site',
        'nickname': 'Nickname',
    }
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp('full_name', csv_fields)
    window.show()
    sys.exit(app.exec_())
