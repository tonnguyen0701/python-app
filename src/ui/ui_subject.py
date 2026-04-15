# -*- coding: utf-8 -*-
from .qt_compat import QtCore, QtGui, QtWidgets

class Ui_SubjectWindow(object):
    def setupUi(self, SubjectWindow):
        SubjectWindow.setObjectName("SubjectWindow")
        SubjectWindow.resize(700, 400)
        self.centralwidget = QtWidgets.QWidget(SubjectWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setObjectName("searchLayout")
        self.searchLabel = QtWidgets.QLabel(self.centralwidget)
        self.searchLabel.setObjectName("searchLabel")
        self.searchLayout.addWidget(self.searchLabel)
        self.searchEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchEdit.setObjectName("searchEdit")
        self.searchLayout.addWidget(self.searchEdit)
        self.mainLayout.addLayout(self.searchLayout)
        self.subjectTable = QtWidgets.QTableWidget(self.centralwidget)
        self.subjectTable.setObjectName("subjectTable")
        self.subjectTable.setColumnCount(4)
        self.subjectTable.setRowCount(0)
        for i in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.subjectTable.setHorizontalHeaderItem(i, item)
        self.mainLayout.addWidget(self.subjectTable)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.buttonLayout.addWidget(self.addButton)
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setObjectName("editButton")
        self.buttonLayout.addWidget(self.editButton)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.buttonLayout.addWidget(self.deleteButton)
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setObjectName("refreshButton")
        self.buttonLayout.addWidget(self.refreshButton)
        self.mainLayout.addLayout(self.buttonLayout)
        SubjectWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(SubjectWindow)
        QtCore.QMetaObject.connectSlotsByName(SubjectWindow)

    def retranslateUi(self, SubjectWindow):
        _translate = QtCore.QCoreApplication.translate
        SubjectWindow.setWindowTitle(_translate("SubjectWindow", "Quản lý môn học"))
        self.searchLabel.setText(_translate("SubjectWindow", "Tìm kiếm:"))
        self.searchEdit.setPlaceholderText(_translate("SubjectWindow", "Nhập tên môn học..."))
        self.addButton.setText(_translate("SubjectWindow", "Thêm môn học"))
        self.editButton.setText(_translate("SubjectWindow", "Sửa"))
        self.deleteButton.setText(_translate("SubjectWindow", "Xóa"))
        self.refreshButton.setText(_translate("SubjectWindow", "Làm mới"))
        headers = ["Mã", "Tên môn học", "Mã", "Số tín chỉ"]
        for idx, text in enumerate(headers):
            self.subjectTable.horizontalHeaderItem(idx).setText(_translate("SubjectWindow", text))
