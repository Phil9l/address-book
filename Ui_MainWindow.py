# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Apr 26 00:14:44 2016
#      by: PyQt5 UI code generator 5.2.1


from PyQt5 import QtCore, QtGui, QtWidgets


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
