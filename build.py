import os
import re
import time
import sys
import pyautogui
import pygetwindow as gw

def extract_valid_name(file_name):
    pattern = re.compile(r'([A-Za-z]{3}\d{6}-\d{2}|\d{6}-\d{2})')
    match = pattern.search(file_name)
    return match.group(0) if match else None

def start_process(directory_path):
    wincopysql_window = gw.getWindowsWithTitle("Photocopy Orders: 1 - Cloud")
    if wincopysql_window:
        wincopysql_window[0].activate()
        time.sleep(1)

    file_paths = [os.path.join(directory_path, file_name) for file_name in os.listdir(directory_path)]
    file_paths.sort(key=lambda x: os.path.getmtime(x))

    for file_path in file_paths:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        matched_name = extract_valid_name(base_name)
        if matched_name:
            pyautogui.write('.')
            time.sleep(0.1)
            pyautogui.write(matched_name)
            time.sleep(0.1)
            pyautogui.press('enter')
            time.sleep(0.1)

    print("List has been built.")
    sys.exit(0)

if __name__ == "__main__":
    # Use the provided directory path, or default to the current directory
    directory_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    # Ensure we have an absolute path
    if not os.path.isabs(directory_path):
        directory_path = os.path.abspath(directory_path)

    # Validate the directory path
    if not os.path.isdir(directory_path):
        print("Invalid directory. Please provide a valid directory path.")
        sys.exit(1)

    start_process(directory_path)
