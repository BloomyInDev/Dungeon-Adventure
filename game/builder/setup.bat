call ..\..\venv\Scripts\activate.bat
echo Activating venv OK

rmdir /S /Q .\dist
rmdir /S /Q .\build
del /Q "Dungeon Adventure.spec"
