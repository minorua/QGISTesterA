@echo off
rem test_osgeo4w64-ltr.bat
rem begin: 2015-10-13

if not exist "output" mkdir output

rem setlocal
call C:\OSGeo4W64\bin\o4w_env.bat > nul
echo  OSGEO4W_ROOT is %OSGEO4W_ROOT%

rem -------------------------------------
rem call "%OSGEO4W_ROOT%"\apps\grass\grass-6.4.3\etc\env.bat
set PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-ltr
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
rem set VSI_CACHE=TRUE
rem set VSI_CACHE_SIZE=1000000
rem set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%OSGEO4W_ROOT%\apps\qt4\plugins
rem -------------------------------------
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python

python ..\run_test.py output\OSGeo4W64_ltr.html
rem endlocal

pause
