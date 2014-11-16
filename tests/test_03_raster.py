# -*- coding: utf-8 -*-
"""QGIS Unit tests for Raster Layer

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Minoru Akagi'
__date__ = '2014-11-16'

import os
import sys

from qgis.core import QgsRasterFileWriter, QgsRasterLayer, QgsRasterPipe

from utilities import (unitTestDataPath,
                       TestCase,
                       unittest,
                       outputDataPath,
                       compareFile,
                       compareFileSet,
                       copyFileSet)

class TC01_Raster(TestCase):

  layerName = "dem"
  fileName = layerName + ".tif"

  def _testAvailable(self):
    return True

  def _testDataPath(self, filename=None, output=False):
    if output:
      return outputDataPath(filename)
    return unitTestDataPath(filename, own=True)

  def _testLayer(self, filename=None, output=False):
    filepath = self._testDataPath(filename, output)
    layer = QgsRasterLayer(filepath, os.path.splitext(os.path.basename(filepath))[0], "gdal")
    assert layer.isValid(), "failed to load layer"
    return layer

  def test01_LoadGeoTIFF(self):
    """Load a GeoTIFF file"""
    self._testAvailable() or self.skipTest("Not available")
    self._testLayer(self.fileName)

  def test02_SaveAsGeoTIFF(self):
    """Save raster layer as a GeoTIFF file"""
    self._testAvailable() or self.skipTest("Not available")

    layer = self._testLayer(self.fileName)

    # write to a GeoTIFF file
    # ref. to the InaSAFE plugin
    provider = layer.dataProvider()
    pipe = QgsRasterPipe()
    assert pipe.set(provider.clone()), "cannot set provider to pipe"

    outfile = self._testDataPath(self.fileName, output=True)
    writer = QgsRasterFileWriter(outfile)
    assert not writer.writeRaster(pipe, provider.xSize(), provider.ySize(), provider.extent(), provider.crs()), "failed to write"
    assert os.path.exists(outfile), "output file cannot be found"


class TC02_RasterFilePath(TC01_Raster):

  subDir = u"ラスタ(ソ)"
  layerName = u"ラスタ(ソ)"
  fileName = layerName + ".tif"

  def _testAvailable(self):
    fse = sys.getfilesystemencoding()
    return self.layerName == self.layerName.encode(fse, "replace").decode(fse, "replace")

  def _testDataPath(self, filename=None, output=False):
    outdir = self.subDir + "_out" if output else self.subDir
    if filename is None:
      return outputDataPath(outdir)
    return outputDataPath(os.path.join(outdir, filename))

  def test001_OS(self):
    """Checks if OS supports file path with Japanese characters"""
    if not self._testAvailable():
      assert 0, "OS cannot handle file path that includes Japanese characters"

  def test002_EnvVars(self):
    """[INFO] Environment Variable(s)"""
    print "GDAL_FILENAME_IS_UTF8=" + os.environ.get("GDAL_FILENAME_IS_UTF8", "")

  def test003_PrepareFiles(self):
    """Prepare files for test"""
    self._testAvailable() or self.skipTest("Not available")

    # if output directory exists, clean up files under it. Otherwise create the output directory with non-ASCII characters
    for b in [False, True]:
      outdir = self._testDataPath(output=b)
      if os.path.exists(outdir):
        for filename in os.listdir(outdir):
          os.remove(os.path.join(outdir, filename))
      else:
        os.mkdir(outdir)

    # copy a set of shapefile
    infile = unitTestDataPath(TC01_Raster.layerName, own=True)
    workfile = self._testDataPath(self.layerName)
    ext_list = [".tif"]
    copyFileSet(infile, workfile, ext_list)


if __name__ == "__main__":
  unittest.main()
