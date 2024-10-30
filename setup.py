import sys
import os
from cx_Freeze import setup, Executable

# Paths for main scripts and additional files
main_gui_script = r"C:\Users\ncurtis\Documents\PROJECTS\!Completed Programs\List Build\main.py"
main_terminal_script = r"C:\Users\ncurtis\Documents\PROJECTS\!Completed Programs\List Build\build.py"
license_file = r"C:\Users\ncurtis\Documents\PROJECTS\!Completed Programs\List Build\LICENSE.txt"
icon_file = r"C:\Users\ncurtis\Documents\PROJECTS\!Completed Programs\List Build\List.ico"

# Path to Anaconda's Qt bin directory
qt_bin_path = r"C:\Users\ncurtis\AppData\Local\anaconda3\Library\bin"

# Include necessary files and directories
include_files = [
    license_file,
    icon_file,
    (qt_bin_path, "bin")  # Copies the entire Qt `bin` directory as a subdirectory named "bin"
]

# Options for the build
build_exe_options = {
    "packages": ["os", "re", "sys", "time", "pyautogui", "pygetwindow", "PyQt5.QtWidgets", "PyQt5.QtCore", "PyQt5.QtGui"],
    "excludes": ["matplotlib", "scipy"],
    "include_files": include_files
}

# Set base for GUI app to "Win32GUI" to hide the terminal window
base = "Win32GUI" if sys.platform == "win32" else None

# Define executables for both the GUI and terminal-based apps
executables = [
    Executable(
        main_gui_script,
        base=base,
        icon=icon_file,
        target_name="List Builder.exe"  # Name of the GUI output executable
    ),
    Executable(
        main_terminal_script,
        base=base,  # Hide terminal for this as well
        target_name="build.exe"  # Name of the terminal-based output executable
    )
]

# Setup configuration
setup(
    name="List Builder Suite",
    author="Nathan Curtis",
    author_email="nathancurtis951@gmail.com",
    license="Proprietary",
    version="2.6",
    description="List Builder 2.6 and associated tools",
    options={"build_exe": build_exe_options},
    executables=executables
)
