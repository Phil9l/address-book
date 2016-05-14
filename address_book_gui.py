#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Apr 26 00:14:44 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from friends import VK_Friend
from utils import VK_API, CSV_Generator


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(431, 483)
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.horizontalLayout.addWidget(self.pushButton)
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
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.comboBox.setItemText(0, _translate("MainWindow", "VK"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Twitter"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "user id"))
        self.pushButton.setText(_translate("MainWindow", "Add Friends"))
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


class MyApp(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, title_field, fields, parent=None, name=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)

        self.title_field = title_field
        self.fields = fields

        self.pushButton.clicked.connect(self.add_frineds)
        self.pushButton_2.clicked.connect(self.save_CSV)

        self.user_id = 0
        # self.add_frineds()

    def get_friends(self):
        user_id = self.lineEdit.text()
        # user_id = '44232785'
        try:
            vk = VK_API()
            self.friend_list = [
                VK_Friend(**friend) for friend in vk.get_friends(user_id)
            ]
            return self.friend_list
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Wrong ID',
                                           'No user with such id found.')
            return []

    def add_frineds(self):
        friends = self.get_friends()
        for friend in friends:
            fields = []
            for field in self.fields:
                if hasattr(friend, field) and getattr(friend, field) != '':
                    fields.append((self.fields[field],
                                  str(getattr(friend, field))))
            self.add_item(self.user_id,
                          str(getattr(friend, self.title_field)), fields)
            self.user_id += 1

    def save_CSV(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Dialog Title',
                                                         'contacts.csv')
        if filename[0]:
            csv_file = CSV_Generator(self.fields)
            csv_file.set_titles(**self.fields)
            for friend in self.friend_list:
                csv_file.add_values(**vars(friend))

            with open(filename[0]) as out_file:
                print(csv_file.get_title(), file=out_file)
                for csv_value in csv_file.get_values():
                    print(csv_value, file=out_file)
            QtWidgets.QMessageBox.critical(self, 'Success',
                                           'Statistics was saved successfuly.')


if __name__ == "__main__":
    csv_fields = {
        'full_name': 'Name',
        'bdate': 'Birthday',
        'phone': 'Mobile Phone',
        'email': 'E-mail Address',
    }
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp('full_name', csv_fields)
    window.show()
    sys.exit(app.exec_())
