# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Users\minorua\.qgis2\python\developing_plugins\QGISTester\qgis_tester_dialog.ui'
#
# Created: Sat Nov 15 10:20:12 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QGISTesterDialog(object):
    def setupUi(self, QGISTesterDialog):
        QGISTesterDialog.setObjectName(_fromUtf8("QGISTesterDialog"))
        QGISTesterDialog.resize(894, 485)
        self.verticalLayout = QtGui.QVBoxLayout(QGISTesterDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.webView = QtWebKit.QWebView(QGISTesterDialog)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonSave = QtGui.QPushButton(QGISTesterDialog)
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.horizontalLayout.addWidget(self.pushButtonSave)
        self.button_box = QtGui.QDialogButtonBox(QGISTesterDialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.horizontalLayout.addWidget(self.button_box)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(QGISTesterDialog)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), QGISTesterDialog.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), QGISTesterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QGISTesterDialog)

    def retranslateUi(self, QGISTesterDialog):
        QGISTesterDialog.setWindowTitle(_translate("QGISTesterDialog", "QGIS Tester", None))
        self.pushButtonSave.setText(_translate("QGISTesterDialog", "保存", None))

from PyQt4 import QtWebKit
