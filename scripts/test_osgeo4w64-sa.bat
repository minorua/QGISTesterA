@echo off
rem test_osgeo4w64-sa.bat
rem begin: 2014-11-14
rem osgeo4w_roots.txt: list of osgeo4w root directories

if not exist "output" mkdir output

setlocal enabledelayedexpansion
set /a "index = 1"
for /F "delims=" %%i in (osgeo4w_roots.txt) do (

for /F "delims=" %%F in ('echo %%i') do set name=%%~nxF
set name=!name:QGIS =!
echo !index!. !name! - %%i

setlocal
call "%%i\bin\o4w_env.bat" > nul
echo  OSGEO4W_ROOT is !OSGEO4W_ROOT!

rem -------------------------------------
rem call "!OSGEO4W_ROOT!"\apps\grass\grass-6.4.3\etc\env.bat
set PATH=!OSGEO4W_ROOT!\apps\qgis\bin;!PATH!
set QGIS_PREFIX_PATH=!OSGEO4W_ROOT:\=/!/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
rem Set VSI cache to be used as buffer, see #6448
rem set VSI_CACHE=TRUE
rem set VSI_CACHE_SIZE=1000000
rem set QT_PLUGIN_PATH=!OSGEO4W_ROOT!\apps\qgis\qtplugins;!OSGEO4W_ROOT!\apps\qt4\plugins
rem -------------------------------------
set PYTHONPATH=!OSGEO4W_ROOT!\apps\qgis\python

python ..\run_test.py output\!index!_!name!.html
echo;
endlocal

set /a "index = index + 1"
)
endlocal

pause
