@echo Start
@echo off
set path=%path%;C:\Python27\
set PYTHONPATH=C:\Python27;C:\Python27\Lib

@echo Creating log14400.html

echo ^<head^> > .\release\log14400.html
echo ^<link rel="stylesheet" href="style.css"^> >> .\release\log14400.html
echo ^<title^>Logik - Webcam Redirect (14400)^</title^> >> .\release\log14400.html
echo ^<style^> >> .\release\log14400.html
echo body { background: none; } >> .\release\log14400.html
echo ^</style^> >> .\release\log14400.html
echo ^<meta http-equiv="Content-Type" content="text/html;charset=UTF-8"^> >> .\release\log14400.html
echo ^</head^> >> .\release\log14400.html

type .\README.md | C:\Python27\python -m markdown -x tables >> .\release\log14400.html

@echo Generate code
cd ..\..
C:\Python27\python generator.pyc "14400-Webcam-Redirect" UTF-8

@echo Copying files
xcopy .\projects\14400-Webcam-Redirect\src .\projects\14400-Webcam-Redirect\release /exclude:.\projects\14400-Webcam-Redirect\src\exclude.txt

@echo Fertig.

@pause