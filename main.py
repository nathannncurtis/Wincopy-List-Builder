import os
import re
import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit,
                             QVBoxLayout, QFileDialog, QProgressBar, QAction, QDialog, QListWidget,
                             QInputDialog)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon
import pyautogui
import pygetwindow as gw

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("Ronsin Photocopy", "List Build")
        self.setWindowTitle("Wincopy List Builder")
        self.setWindowIcon(QIcon('List.ico'))
        self.setGeometry(100, 100, 515, 200)
        self.setFixedSize(515, 200)
        self.dark_mode = self.settings.value("darkMode", type=bool)
        self.apply_theme()
        self.variables = self.settings.value("variables", [], type=list)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setAlignment(Qt.AlignCenter)

        self.menu_bar = self.menuBar()
        extras_menu = self.menu_bar.addMenu("Extras")

        self.toggle_theme_action = QAction("Toggle Theme", self)
        self.toggle_theme_action.setCheckable(True)
        self.toggle_theme_action.setChecked(self.dark_mode)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        extras_menu.addAction(self.toggle_theme_action)

        self.toggle_close_action = QAction("Close After List is Finished", self)
        self.toggle_close_action.setCheckable(True)
        self.toggle_close_action.setChecked(self.settings.value("closeAfter", type=bool))
        self.toggle_close_action.triggered.connect(self.toggle_close_after_list)
        extras_menu.addAction(self.toggle_close_action)

        variables_action = QAction("Variables", self)
        variables_action.triggered.connect(self.show_variables_dialog)
        extras_menu.addAction(variables_action)

        about_action = QAction("About", self)
        extras_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about_dialog)

        self.directory_entry = QLineEdit(self)
        self.directory_entry.setPlaceholderText("Enter the directory path or browse for the folder")
        layout.addWidget(self.directory_entry)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_directory)
        layout.addWidget(browse_button)

        start_button = QPushButton("Build List", self)
        start_button.clicked.connect(self.start_process)
        layout.addWidget(start_button)

        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

    def toggle_close_after_list(self, checked):
        self.settings.setValue("closeAfter", checked)

    def toggle_theme(self, checked):
        self.dark_mode = checked
        self.settings.setValue("darkMode", self.dark_mode)
        self.apply_theme()

    def browse_directory(self):
        directory_path = QFileDialog.getExistingDirectory(self, "Select a directory")
        if directory_path:
            self.directory_entry.setText(directory_path)

    def start_process(self):
        directory_path = self.directory_entry.text()
        if directory_path:
            wincopysql_window = gw.getWindowsWithTitle("Photocopy Orders: 1 - Default Company Name")
            if wincopysql_window:
                wincopysql_window[0].activate()
                time.sleep(1)
            file_paths = [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path)]
            file_paths.sort(key=lambda x: os.path.getmtime(x))
            self.progress_bar.setMaximum(len(file_paths))
            for i, file_path in enumerate(file_paths):
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                matched_name = self.extract_valid_name(base_name)
                if matched_name:
                    pyautogui.write('.')
                    time.sleep(0.1)
                    pyautogui.write(matched_name)
                    time.sleep(0.1)
                    pyautogui.press('enter')
                    time.sleep(0.1)
                self.progress_bar.setValue(i + 1)
            self.result_label.setText("List has been built.")
        else:
            self.result_label.setText("Please enter a valid directory path")

    def show_variables_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Variables")
        dialog.setFixedSize(400, 300)
        layout = QVBoxLayout(dialog)

        list_widget = QListWidget(dialog)
        list_widget.addItems(self.variables)
        layout.addWidget(list_widget)

        add_button = QPushButton("Add Variable", dialog)
        add_button.clicked.connect(lambda: self.add_variable(list_widget))
        layout.addWidget(add_button)

        remove_button = QPushButton("Remove Selected", dialog)
        remove_button.clicked.connect(lambda: self.remove_variable(list_widget))
        layout.addWidget(remove_button)

        dialog.exec_()

    def add_variable(self, list_widget):
        text, ok = QInputDialog.getText(self, 'Add Variable', 'Enter a new variable:')
        if ok and text:
            self.variables.append(text)
            self.settings.setValue("variables", self.variables)
            list_widget.addItem(text)

    def remove_variable(self, list_widget):
        for item in list_widget.selectedItems():
            self.variables.remove(item.text())
            list_widget.takeItem(list_widget.row(item))
        self.settings.setValue("variables", self.variables)

    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About List Builder")
        about_dialog.setFixedSize(300, 200)
        about_dialog_layout = QVBoxLayout()
        label = QLabel("Wincopy List Builder \n\nVersion 2.0 - April 27th, 2024\n© Ronsin Photocopy\nAll rights reserved.")
        about_dialog_layout.addWidget(label)
        about_dialog.setLayout(about_dialog_layout)
        about_dialog.exec_()

    def is_valid_file(self, file_name):
        # Strip any prefix or postfix variable strings from the filename
        for var in self.variables:
            if file_name.startswith(var):
                file_name = file_name[len(var):].strip()  # Remove prefix
            elif file_name.endswith(var):
                file_name = file_name[:-len(var)].strip()  # Remove postfix

        # Regex pattern to match the cleaned filename
        pattern = re.compile(r'^([A-Za-z]{3}\d{6}-\d{2}|\d{6}-\d{2})$')
        return pattern.match(file_name) is not None

    def extract_valid_name(self, file_name):
        # Strip any prefix or postfix variable strings from the filename
        for var in self.variables:
            if file_name.startswith(var):
                file_name = file_name[len(var):].strip()
            elif file_name.endswith(var):
                file_name = file_name[:-len(var)].strip()

        # This will capture the exact part of the filename that matches the regex
        pattern = re.compile(r'([A-Za-z]{3}\d{6}-\d{2}|\d{6}-\d{2})')
        match = pattern.search(file_name)
        return match.group(0) if match else None

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QDialog {
                    background-color: #333;
                    color: white;
                }
                QLineEdit, QPushButton, QProgressBar, QMenuBar, QMenu, QListWidget {
                    background-color: #555;
                    color: white;
                }
                QLabel {
                    color: white;
                }
                QProgressBar {
                    border: 1px solid #666;
                    background-color: #333;
                }
                QProgressBar::chunk {
                    background-color: #06b;
                }
                QMenuBar::item:selected {
                    background-color: #06b;
                }
                QMenu::item:selected {
                    background-color: #06b; /* Updated highlight color for dark mode */
                    color: white;
                }
                QLineEdit:focus {
                    background-color: #666;
                }
                QListWidget::item:selected {
                    background-color: #767676; /* Noticeably different highlight color */
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QDialog {
                    background-color: #eee;
                    color: black.
                }
                QLineEdit, QPushButton, QProgressBar, QMenuBar, QMenu, QListWidget {
                    background-color: #ccc;
                    color: black.
                }
                QLabel {
                    color: black.
                }
                QProgressBar {
                    border: 1px solid #bbb;
                    background-color: #eee;
                }
                QProgressBar::chunk {
                    background-color: #06b;
                }
                QMenuBar::item:selected {
                    background-color: #a0c4ff;
                }
                QMenu::item:selected {
                    background-color: #a0c4ff; /* Updated highlight color for light mode */
                    color: black.
                }
                QLineEdit:focus {
                    background-color: #ddd;
                }
                QListWidget::item:selected {
                    background-color: #dcdcdc; /* Lighter color for selection highlight */
                    color: black.
                }
            """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())