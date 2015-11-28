# -*- coding: utf-8 -*-
"""QGIS unit tests for vector layer

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Minoru Akagi'
__date__ = '2014-11-16'

import os
import sys

from PyQt4.QtCore import QSettings, QVariant, qDebug
from qgis.core import QGis, QgsFeature, QgsField, QgsVectorLayer, QgsVectorFileWriter

from utilities import (unitTestDataPath,
                       TestCase,
                       unittest,
                       outputDataPath,
                       setSettingValue,
                       restoreSettings,
                       compareFile,
                       compareFileSet,
                       copyFileSet)

debug_mode = False


class TC01_Attribute(TestCase):

  layerName = "points"
  fileName = layerName + ".shp"

  @classmethod
  def testDataPath(cls, filename=None, output=False):
    if output:
      return outputDataPath(filename)
    return unitTestDataPath(filename, own=True)

  def _testAvailable(self):
    return True

  def _testLayer(self, filename=None, output=False):
    filepath = self.testDataPath(filename, output)
    layer = QgsVectorLayer(filepath, os.path.splitext(os.path.basename(filepath))[0], "ogr")
    assert layer.isValid(), "failed to load layer"
    layer.setProviderEncoding("SJIS")   #tr
    return layer

  if debug_mode:
    def test000_Debug(self):
      print "input directory:", self.testDataPath()
      print "output directory:", self.testDataPath(output=True)

  def test01_LoadShapefile(self):
    """Load a shapefile with non-ASCII characters in attributes"""
    self._testAvailable() or self.skipTest("Not available")
    fieldName = u'\u6587\u5b57\u5217'
    expected = u'\u3042\u3044\u3046\u3048\u304a'

    for ignore in [True, False]:
      setSettingValue("/qgis/ignoreShapeEncoding", ignore)

      # load a shapefile and check its attribute value
      layer = self._testLayer(self.fileName)
      f = layer.getFeatures().next()
      #f = self._testLayer().getFeatures().next()    # crashes 2.0.1 (Win, standalone, 64bit)
      val = f.attribute(fieldName)
      self.assertEqual(val, expected)
      print 'with "ignore..." option = {}...success'.format(ignore)

  def test02_SaveAsShapefile(self):
    """Save layer to a shapefile"""
    self._testAvailable() or self.skipTest("Not available")
    for ignore in [True, False]:
      setSettingValue("/qgis/ignoreShapeEncoding", ignore)

      # load a shapefile and save it to a new shapefile
      layer = self._testLayer(self.fileName)
      outfile = self.testDataPath(u"{}{}.shp".format(self.layerName, 1 if ignore else 2), output=True)
      QgsVectorFileWriter.writeAsVectorFormat(layer, outfile, "SJIS", layer.crs())

      # compare file set
      infile = self.testDataPath(self.fileName)
      c = compareFileSet(os.path.splitext(infile)[0], os.path.splitext(outfile)[0],
                         [".shp", ".shx", ".dbf", ".prj", ".cpg"])
                         #[".dbf", ".cpg"])
      self.assertEqual(c, [], "input and output do not match: {}".format(str(c)))
      print 'with "ignore..." option = {}...success'.format(ignore)

  def test03_SaveAsCSV(self):
    """Save layer to a CSV file"""
    self._testAvailable() or self.skipTest("Not available")
    layer = self._testLayer(self.fileName)
    outfile = self.testDataPath(u"{}.csv".format(self.layerName), output=True)
    QgsVectorFileWriter.writeAsVectorFormat(layer, outfile, "UTF-8", layer.crs(),
                                            "CSV", layerOptions=["LINEFORMAT=LF", "GEOMETRY=AS_XY"])
    expfile = unitTestDataPath("{}.csv".format(TC01_Attribute.layerName), own=True)
    assert compareFile(outfile, expfile, delimiter=",") == 0, "unexpected csv output"

  def test04_EditShapefile1(self):
    """Load a file, edit and overwrite. edits: add a field, set values to the field, and then remove the field"""
    self._testAvailable() or self.skipTest("Not available")
    fieldName = u'\u6587\u5b57\u52172'
    c0 = ord(u'\u30a2')

    infile = self.testDataPath(self.layerName)
    for ignore in [True, False]:
      setSettingValue("/qgis/ignoreShapeEncoding", ignore)

      # copy a set of shapefile
      layerName = u"{}_edit{}".format(self.layerName, 1 if ignore else 2)
      workfile = self.testDataPath(layerName, output=True)
      copyFileSet(infile, workfile, [".shp", ".shx", ".dbf", ".prj", ".cpg"])

      # load the copy
      layer = self._testLayer(workfile + ".shp", output=True)

      # add a field
      layer.startEditing()
      f = QgsField(fieldName, QVariant.String, len=20)
      assert layer.addAttribute(f), "failed to add a field"
      fldIdx = layer.fieldNameIndex(fieldName)

      # set strings with Japanese characters to the field
      c = c0
      for f in layer.getFeatures():
        val = "".join([unichr(c + i) for i in range(5)])
        assert layer.changeAttributeValue(f.id(), fldIdx, val), "failed to change attribute value"
        c += 5

      # save and reload the shapefile
      assert layer.commitChanges(), "failed to commit changes"
      del layer
      layer = self._testLayer(workfile + ".shp", output=True)

      # check the values of the field
      c = c0
      for f in layer.getFeatures():
        val = "".join([unichr(c + i) for i in range(5)])
        self.assertEqual(f.attribute(fieldName), val)
        c += 5

      # remove the added field
      layer.startEditing()
      layer.deleteAttribute(fldIdx)
      assert layer.commitChanges(), "failed to commit changes"

      # compare the file set with source
      c = compareFileSet(infile, workfile, [".shp", ".shx", ".dbf", ".prj", ".cpg"])
      self.assertEqual(c, [], "input and output do not match: {}".format(str(c)))

      print 'with "ignore..." option = {}...success'.format(ignore)

  def test05_EditShapefile2(self):
    """Load a file, remove a record and overwrite
         edits: remove a record
    """
    self._testAvailable() or self.skipTest("Not available")
    setSettingValue("/qgis/ignoreShapeEncoding", True)

    infile = self.testDataPath(self.layerName)
    exfile = TC01_Attribute.testDataPath('expected/' + TC01_Attribute.layerName)

    # copy a set of shapefile
    layerName = u"{}_del".format(self.layerName)
    workfile = self.testDataPath(layerName, output=True)
    copyFileSet(infile, workfile, [".shp", ".shx", ".dbf", ".prj", ".cpg"])

    # load the copy
    layer = self._testLayer(workfile + ".shp", output=True)

    # remove the first record
    layer.startEditing()
    assert layer.deleteFeature(0), "failed to delete a feature"

    # save
    assert layer.commitChanges(), "failed to commit changes"

    # close the layer
    del layer

    # compare the file set with source
    c = compareFileSet(workfile, exfile, [".shp", ".shx", ".dbf", ".prj", ".cpg"])
    self.assertEqual(c, [], "output and expected dataset do not match: {}".format(str(c)))


  #def testxx_CreateShapefile(self):
  #  """Create an empty shapefile"""
  #  self.skipTest("Not available")    # createEmptyDataSource() is not available from Python

  def test99_RestoreSettings(self):
    """Restore settings"""
    restoreSettings()


class TC02_VectorFilePath(TC01_Attribute):

  subDir = u'\u30d9\u30af\u30bf(\u30bd)'
  layerName = u'\u30d9\u30af\u30bf(\u30bd)'
  fileName = layerName + ".shp"

  @classmethod
  def testDataPath(cls, filename=None, output=False):
    outdir = cls.subDir + "_out" if output else cls.subDir
    if filename is None:
      return outputDataPath(outdir)
    return outputDataPath(os.path.join(outdir, filename))

  def _testAvailable(self):
    fse = sys.getfilesystemencoding()
    return self.layerName == self.layerName.encode(fse, "replace").decode(fse, "replace")

  def test001_OS(self):
    """Checks if OS supports file path with Japanese characters"""
    assert self._testAvailable(), "OS cannot handle file path that includes Japanese characters"

  def test002_EnvVars(self):
    """[INFO] Environment Variable(s)"""
    print "GDAL_FILENAME_IS_UTF8=" + os.environ.get("GDAL_FILENAME_IS_UTF8", "")

  def test003_PrepareFiles(self):
    """Prepare files for test"""
    self._testAvailable() or self.skipTest("Not available")

    # if output directory exists, clean up files under it. Otherwise create the output directory with non-ASCII characters
    for b in [False, True]:
      outdir = self.testDataPath(output=b)
      if os.path.exists(outdir):
        for filename in os.listdir(outdir):
          os.remove(os.path.join(outdir, filename))
      else:
        os.mkdir(outdir)

    # copy a set of shapefile
    infile = unitTestDataPath(TC01_Attribute.layerName, own=True)
    workfile = self.testDataPath(self.layerName)
    ext_list = [".shp", ".shx", ".dbf", ".prj", ".cpg"]
    copyFileSet(infile, workfile, ext_list)

if __name__ == "__main__":
  unittest.main()
