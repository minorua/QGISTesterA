# -*- coding: utf-8 -*-
"""
/***************************************************************************
 utilities.py
                                 A QGIS plugin
 Make testing on various platforms easy and reliable
                              -------------------
        begin                : 2014-11-16
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
import shutil
import sys
import unittest
TestCase = unittest.TestCase

from PyQt4.QtCore import QFile, QSettings, qDebug

log_to_stdout = True
_changedSettings = {}

def getQgisTestApp():
  """return QGISAPP, CANVAS, IFACE, PARENT"""
  import qgis
  iface = qgis.utils.iface
  return None, iface.mapCanvas(), iface, iface.mainWindow()

def unitTestDataPath(theSubdir=None, own=False):
  mydir = os.path.dirname(QFile.decodeName(__file__))
  datadir = "data" if own else "testdata"
  if theSubdir is None:
    return os.path.join(mydir, datadir)
  return os.path.join(mydir, datadir, theSubdir)

def outputDataPath(theSubdir=None):
  mydir = os.path.dirname(QFile.decodeName(__file__))
  outdir = "output"
  if theSubdir is None:
    return os.path.join(mydir, outdir)
  return os.path.join(mydir, outdir, theSubdir)

def log(msg):
  if isinstance(msg, unicode):
    qDebug(msg.encode("utf-8"))
    if log_to_stdout:
      print msg.encode(sys.getfilesystemencoding())
  else:
    qDebug(str(msg))
    if log_to_stdout:
      print msg

def setSettingValue(key, value):
  import sip
  assert sip.getapi("QVariant") == 2
  log("#set {} = {}".format(key, value))

  settings = QSettings()
  if not key in _changedSettings:
    _changedSettings[key] = settings.value(key)
  settings.setValue(key, value)

def restoreSettings():
  settings = QSettings()
  for key, value in _changedSettings.iteritems():
    if value is None:
      # remove the key
      settings.remove(key)
      log("#remove key {}".format(key))
    else:
      # set the value before the change
      settings.setValue(key, value)
      log("#reset {} = {}".format(key, value))

  _changedSettings.clear()

def compareFile(file1, file2, text_mode=False, delimiter=None):
  if not os.path.exists(file1) or not os.path.exists(file2):
    return -1

  if delimiter is None:
    with open(file1, "rb") as f:
      f1 = f.read()
    with open(file2, "rb") as f:
      f2 = f.read()
    if text_mode:
      f1 = f1.replace("\r\n", "\n")
      f2 = f2.replace("\r\n", "\n")
    return 0 if f1 == f2 else 1

  # dsv mode
  import csv
  rows1 = list(csv.reader(open(file1, "rb"), delimiter=delimiter))
  rows2 = list(csv.reader(open(file2, "rb"), delimiter=delimiter))
  if len(rows1) != len(rows2):
    return 1
  for row1, row2 in zip(rows1, rows2):
    if len(row1) != len(row2):
      return 1
    for val1, val2 in zip(row1, row2):
      try:
        v1 = float(val1)
        v2 = float(val2)
      except:
        if val1 != val2:
          return 1
      else:
        if v1 != v2:
          return 1
  return 0

def compareFileSet(root1, root2, ext_list, text_mode=False, delimiter=None):
  diff_exts = []
  #filetitle = os.path.basename(root1)
  for ext in ext_list:
    if compareFile(root1 + ext, root2 + ext, text_mode, delimiter):
      diff_exts.append(ext)
  return diff_exts

def copyFileSet(root1, root2, ext_list):
  for ext in ext_list:
    shutil.copyfile(root1 + ext, root2 + ext)
