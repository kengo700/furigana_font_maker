@echo off
set FF=C:\Program Files (x86)\FontForgeBuilds
set "PYTHONHOME=%FF%"
set "PYTHONPATH=%FF%lib\python2.7"
set "PATH=%FF%;%FF%\bin;%PATH%"
set FF_PATH_ADDED=TRUE
set CURRENTPATH=%~dp0
ffpython %CURRENTPATH%\furigana_font_maker.py C:\Windows\Fonts\times.ttf C:\Temp\ffm\times_test.ttf
pause