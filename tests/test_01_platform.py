# -*- coding: utf-8 -*-
"""QGIS Unit tests

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Minoru Akagi'
__date__ = '2014-11-16'

import sys

from utilities import (TestCase,
                       unittest)

class TC01_Platform(TestCase):

  @classmethod
  def setUpClass(cls):
    pass

  @classmethod
  def tearDownClass(cls):
    pass

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test01_QGIS(self):
    """[INFO] QGIS information"""
    from qgis.core import QGis
    print "version: {} ({})".format(QGis.QGIS_VERSION, QGis.QGIS_DEV_VERSION)

  def test02_Qt(self):
    """[INFO] Qt information"""
    from PyQt4.QtCore import QT_VERSION_STR
    print "Qt version:", QT_VERSION_STR

    try:
      from PyQt4.pyqtconfig import Configuration
      cfg = Configuration()
      print "SIP version:", cfg.sip_version_str
      print "PyQt version:", cfg.pyqt_version_str

    except:
      from PyQt4.Qt import PYQT_VERSION_STR
      from sip import SIP_VERSION_STR
      print "SIP version:", SIP_VERSION_STR
      print "PyQt version:", PYQT_VERSION_STR

  def test03_Python(self):
    """[INFO] Python information"""
    print "sys.version:", sys.version

  def test04_OS(self):
    """[INFO] OS information"""
    import platform
    print platform.platform()


class TC02_Encoding(TestCase):

  def test01_PythonInfo(self):
    """[INFO] Python encoding information"""
    print "sys.getdefaultencoding:", sys.getdefaultencoding()
    print "sys.getfilesystemencoding:", sys.getfilesystemencoding()

  def test02_Qt_SJIS(self):
    """Checks if SJIS encoding is available with Qt installation"""
    from PyQt4.QtCore import QTextCodec
    self.assertIn("SJIS", QTextCodec.availableCodecs())
    print "SJIS is available"


if __name__ == "__main__":
  unittest.main()
