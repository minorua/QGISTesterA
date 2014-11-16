# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGISTester
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
import os

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFile
from PyQt4.QtGui import QAction, QIcon

debug_mode = 1

class QGISTester:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    # initialize plugin directory
    self.plugin_dir = os.path.dirname(QFile.decodeName(__file__))
    # initialize locale
    locale = QSettings().value('locale/userLocale')[0:2]
    locale_path = os.path.join(self.plugin_dir, 'i18n', 'QGISTester_{}.qm'.format(locale))
    if os.path.exists(locale_path):
      self.translator = QTranslator()
      self.translator.load(locale_path)

      if qVersion() > '4.3.3':
        QCoreApplication.installTranslator(self.translator)

    # Declare instance attributes
    self.menu = self.tr("&QGIS Tester")

  def tr(self, message):
    """Get the translation for a string using Qt translation API."""
    return QCoreApplication.translate('QGISTester', message)

  def initGui(self):
    # Create action that will start plugin configuration
    icon_path = os.path.join(self.plugin_dir, "icon.png")
    self.action = QAction(QIcon(icon_path), self.tr("Test your QGIS!"), self.iface.mainWindow())
    self.action.setObjectName("QGISTester_Test")

    # Connect the action to the run method
    self.action.triggered.connect(self.run)

    # Add toolbar button and menu item
    self.iface.addPluginToMenu(self.menu, self.action)
    if debug_mode:
      self.iface.addToolBarIcon(self.action)

  def unload(self):
    """Remove the plugin menu item and icon"""
    self.iface.removePluginMenu(self.menu, self.action)
    if debug_mode:
      self.iface.removeToolBarIcon(self.action)

  def run(self):
    # Import the code for the dialog
    from qgis_tester_dialog import QGISTesterDialog

    # Create the dialog
    dlg = QGISTesterDialog()
    # show the dialog
    dlg.show()
    # Run the dialog event loop
    dlg.exec_()
