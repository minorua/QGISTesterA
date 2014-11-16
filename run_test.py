# -*- coding: utf-8 -*-
"""
/***************************************************************************
 run_test.py

 Make testing on various platforms easy and reliable
                             -------------------
        begin                : 2014-11-14
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
import sys
if __name__ == "__main__":
  import sip
  try:
    for api in ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]:
      sip.setapi(api, 2)
  except Exception as e:
    print "Failed to set sip api version"
    print e.message
    sys.exit(1)
  stdout = sys.stdout

import datetime
import imp
import os

from qgis_test_result import QGISTestResult
from tests import utilities as utils

def runTest():
  unittest = utils.unittest
  plugin_dir = os.path.dirname(__file__.decode(sys.getfilesystemencoding()))
  plugin_name = os.path.basename(plugin_dir)
  test_dir = os.path.join(plugin_dir, "tests")
  temp_dir = utils.outputDataPath()

  # if the output directory exists, clean up files under it. Otherwise create the output directory
  if os.path.exists(temp_dir):
    for filename in os.listdir(temp_dir):
      filepath = os.path.join(temp_dir, filename)
      if os.path.isfile(filepath):
        os.remove(filepath)
  else:
    os.mkdir(temp_dir)

  # append the tests directory to the python path list temporarily
  sys.path.append(test_dir)

  loader = unittest.TestLoader()
  #suite = unittest.TestLoader().discover(".".join([plugin_name, "tests"]))
  suite = unittest.TestSuite()
  result = QGISTestResult()
  result.appendLog("Test started running: " + str(datetime.datetime.now()))
  result.appendLog("output directory: " + temp_dir)

  for filename in os.listdir(test_dir):
    file = os.path.join(test_dir, filename)
    if os.path.isfile(file) and filename.startswith("test") and filename.endswith(".py"):
      mod = imp.load_source(os.path.splitext(filename)[0], file)
      suite.addTest(loader.loadTestsFromModule(mod))
      result.appendLog("{} loaded".format(filename))
  result.appendLog("\n")

  suite.run(result)

  # remove the tests directory from the python path list
  sys.path.remove(test_dir)

  return result

if __name__ == "__main__":
  def usage():
    print "Usage:"
    print "    run_test.py output_file_path"
    sys.exit(1)
  
  from PyQt4.QtCore import QSize
  from PyQt4.QtGui import QWidget

  from qgis.core import QgsApplication

  if len(sys.argv) < 2:
    print "Output file path is not specified."
    usage()
  outfile = sys.argv[-1]

  myGuiFlag = True  # All test will run qgis in gui mode
  QGISAPP = QgsApplication(sys.argv, myGuiFlag)
  QGISAPP.initQgis()
  s = QGISAPP.showSettings()

  result = runTest()
  with open(outfile, "w") as f:
    f.write(result.html())
  sys.stdout = stdout
  print ""
  print "Result written to", outfile
