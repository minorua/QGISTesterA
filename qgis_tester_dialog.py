# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGISTesterDialog
                                 A QGIS plugin
 Make testing on various platforms easy and reliable
                             -------------------
        begin                : 2014-11-09
        copyright            : (C) 2014 Minoru Akagi
        email                : akaginch@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import imp
import os
import sys

from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox

from ui_qgis_tester_dialog import Ui_QGISTesterDialog


class QGISTesterDialog(QDialog):
  def __init__(self, parent=None):
    QDialog.__init__(self, parent)

    self.html = ""

    # Set up the user interface from Designer.
    self.ui = ui = Ui_QGISTesterDialog()
    ui.setupUi(self)

    ui.pushButtonSave.clicked.connect(self.saveResult)

    # run test!
    self.runTest()

  def runTest(self):
    from run_test import runTest
    result = runTest()
    self.html = result.html()
    self.ui.webView.setHtml(self.html)

  def saveResult(self):
    filename = QFileDialog.getSaveFileName(self, "Save result to a HTML file", filter="HTML (*.html *.htm)")
    if not filename:
      return

    with open(filename, "w") as f:
      f.write(self.html)

    QMessageBox.information(self, "QGISTester", "Result has been saved to: {}".format(filename))
