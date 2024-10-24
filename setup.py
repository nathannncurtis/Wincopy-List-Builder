import sys
from cx_Freeze import setup, Executable

# Specify the path of your files
main_script = r"C:\Users\ncurtis\3D Objects\BATCH\xtra\programs\List Build 2.0\main.py"
license_file = r"C:\Users\ncurtis\3D Objects\BATCH\xtra\programs\List Build 2.0\LICENSE.txt"
icon_file = r"C:\Users\ncurtis\3D Objects\BATCH\xtra\programs\List Build 2.0\List.ico"

# Options for the build
build_exe_options = {
    "packages": ["os", "re", "sys", "time", "pyautogui", "pygetwindow", "PyQt5.QtWidgets", "PyQt5.QtCore", "PyQt5.QtGui"],
    "excludes": ["matplotlib", "scipy"],
    "include_files": [license_file, icon_file]  # Including additional files like license and icon
}

# Determine the base
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Define the executable
executables = [
    Executable(
        main_script,
        base=base,
        icon=icon_file,
        target_name="List Builder.exe"  # Name of the output executable
    )
]

# Setup configuration
setup(
    name="List Builder",
    author="Nathan Curtis",
    author_email="nathancurtis951@gmail.com",
    license="Proprietary",
    version="2.0",
    description="List Builder 2.0",
    options={"build_exe": build_exe_options},
    executables=executables
)
