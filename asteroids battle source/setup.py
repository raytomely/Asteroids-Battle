import sys
from cx_Freeze import setup, Executable

build_exe_options = {'include_files': ['asteroids_battle_data'], "excludes": ["tkinter"]}


setup(
    name ='asteroids battle',
    author='rdn',
    version = '1.0',
    options={'build_exe': build_exe_options},
    executables = [Executable('asteroids_battle.py', base = 'Win32GUI',icon = 'rocket.ico')])




#in command line(cmd)  change to current directory(cd) and write: "setup.py build" or "setup.py build_exe"
