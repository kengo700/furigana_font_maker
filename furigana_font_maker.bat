@echo off
set FF=C:\Program Files (x86)\FontForgeBuilds
set "PYTHONHOME=%FF%"
set "PYTHONPATH=%FF%lib\python2.7"
set "PATH=%FF%;%FF%\bin;%PATH%"
set FF_PATH_ADDED=TRUE
set CURRENTPATH=%~dp0
set SRC_TEXT=dummy_text.txt
set SRC_FONT=C:\Windows\Fonts\yumin.ttf
set DST_TEXT=dummy_text_furigana.txt
set DST_FONT=C:\Temp\ffm\yumin_furigana.ttf
ffpython %CURRENTPATH%\furigana_font_maker.py %SRC_TEXT% %SRC_FONT% %DST_TEXT% %DST_FONT%
pause