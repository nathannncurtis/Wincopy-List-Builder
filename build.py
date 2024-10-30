import os
import re
import time
import sys
import shlex
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
    if len(sys.argv) < 2:
        print("Please provide a directory path.")
        sys.exit(1)

    # Join all arguments in case the path has spaces without quotes
    args = " ".join(sys.argv[1:])
    split_args = shlex.split(args)  # Split intelligently to handle quotes

    directory_path = split_args[0]  # The first (and only) argument after processing

    if not os.path.isdir(directory_path):
        print("Invalid directory. Please provide a valid directory path.")
        sys.exit(1)

    start_process(directory_path)
