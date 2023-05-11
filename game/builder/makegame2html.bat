call .\setup.bat
rmdir /S /Q .\dist
rmdir /S /Q .\build
pyxel package ..\game ..\game\main.py
pyxel app2html game