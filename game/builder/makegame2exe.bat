call .\setup.bat
pyinstaller --noconfirm --onefile --windowed --name "Dungeon Adventure" --hidden-import "pyxel" --add-data "../ressources.pyxres;."  "../main.py"