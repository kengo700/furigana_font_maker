@echo off
set FF=C:\Program Files (x86)\FontForgeBuilds
set "PYTHONHOME=%FF%"
set "PYTHONPATH=%FF%lib\python2.7"
set "PATH=%FF%;%FF%\bin;%PATH%"
set FF_PATH_ADDED=TRUE
set CURRENTPATH=%~dp0
set CONFIG_FILE=config.ini
ffpython %CURRENTPATH%\furigana_font_maker.py %CONFIG_FILE%
pause