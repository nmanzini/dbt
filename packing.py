import sys
from cx_Freeze import setup, Executable

'''
To pack the program go to cmd in the folder and type:
python packing.py build

to pack it into an installer, open cmd in the folder and type:
python packing.py bdist_msi
'''


application_title = "Desktop background Tool" #what you want to application to be called
main_python_file = "gui.py" #the name of the python file you use to run the program

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["atexit","re"]

setup(
        name = application_title,
        version = "0.1",
        description = "Sample cx_Freeze PyQt4 script",
        options = {"build_exe" : {"includes" : includes }},
        executables = [Executable(main_python_file, base = base)])