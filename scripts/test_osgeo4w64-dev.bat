@echo off
rem test_osgeo4w64-dev.bat
rem begin: 2014-11-18

if not exist "output" mkdir output

rem setlocal
call C:\OSGeo4W64\bin\o4w_env.bat > nul
echo  OSGEO4W_ROOT is %OSGEO4W_ROOT%

rem -------------------------------------
rem call "%OSGEO4W_ROOT%"\apps\grass\grass-6.4.3\etc\env.bat
set PATH=%OSGEO4W_ROOT%\apps\qgis-dev\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-dev
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
rem set VSI_CACHE=TRUE
rem set VSI_CACHE_SIZE=1000000
rem set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-dev\qtplugins;%OSGEO4W_ROOT%\apps\qt4\plugins
rem -------------------------------------
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-dev\python

python ..\run_test.py output\OSGeo4W64_dev.html
rem endlocal

pause
