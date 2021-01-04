#!/usr/bin/env python3

try:
    import tkinter as tk
    from tkinter import messagebox as msg
except:
    import Tkinter as tk
    from Tkinter import messagebox as msg
import os, sys
import signal
import time
import multiprocessing
from pathlib import Path
from PIL import Image, ImageTk
# Use pip3 install watchdog to install watchdog 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


directories_to_watch = ["C:\\Users\\explo\\Documents", "C:\\xampp\\htdocs", "F:\\laravel-apps", "F:\\All Courses Mike"]
path_to_write = "C:\\Users\\explo\\Desktop" # Ensure path is not included in watched directory above
file_name = "filesystem_monitoring.txt"
storage_path = path_to_write + '\\' + file_name
# Replace path to "main.py" with your systems path to "main.py" to start program when you Login
start_file_on_login_path = "C:\\Users\\explo\\Documents\\Python_Projects\\filesystem_monitoring\\src\\main.py"
# Replace with your startup folder path -> press WinKey + R, then type shell:startup and hit enter to get path.
startup_path = 'C:\\Users\\explo\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'

def check_path_exists(path):
    if not os.path.exists(path):
        msg.showerror('Path Error!', f"[ !! ]The Path to write directory {path} does not exist.")
        sys.exit(1)
    else:
        pass

# Check that paths exists
check_path_exists(path_to_write)
check_path_exists(start_file_on_login_path)
check_path_exists(startup_path)

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # Take any action here when a file is created.
        with open(storage_path, 'a') as file:
            file.write(f"[++] Created {event.src_path}")
            file.write("\n")
    def on_deleted(self, event):
        # Take any action here when a file is deleted.
        with open(storage_path, 'a') as file:
            file.write(f"[!!] Deleted {event.src_path}")
            file.write("\n")
    def on_moved(self, event):
        # Take any action here when a file is moved (Renamed).
        with open(storage_path, 'a') as file:
            file.write(f"[>>] Renamed {event.src_path} to {event.dest_path}")
            file.write("\n")

b1 = ''
event_handler = Handler()
observer = Observer()
window = tk.Tk()

def add_to_startup(startup_path, file_path):
    with open(startup_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(f'python {file_path}')

def dir_watcher(watch_directory):
    observer.schedule(event_handler, watch_directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        print(f"[+] Saved output to {path_to_write}\{file_name}")
        print("[-] Stopped Observer and Caught Exception (KeyboardInterrupt).")
    observer.join()

process_ids = []
def start_observer():
    global b1
    global process_ids
    msg.showinfo('Starting Observer', 'Monitoring will begin in the background if path(s) exist')
    b1["text"] = "Started Monitoring"
    b1["state"] = "disabled"
    b1["cursor"] = "arrow"
    for watch_directory in directories_to_watch:
        if not os.path.exists(watch_directory.strip(' ')):
            msg.showerror('Path Error!', f"[ !! ] The Directory or Path {watch_directory} does not exist. Restart program after fixing path.")
            stop_observer()
            break
        mp = multiprocessing.Process(target=dir_watcher, args=(watch_directory.strip(' '),))
        mp.start()
        process_ids.append(mp.pid)

def stop_observer():
    global b1
    global process_ids
    for kill_id in process_ids:
        os.kill(kill_id, signal.SIGINT)
    process_ids = []
    b1["text"] = "Start monitoring"
    b1["state"] = "normal"
    b1["cursor"] = "hand2"
    msg.showinfo('Stopping Observer', f"[ - ] All Observers have been stopped.")

def exit_application():
    response = msg.askyesno('Close Application', f'Are you sure you want to exit the application? \n\n "YES" - by clicking "Yes", the app will close and all observers will be stopped. \n\n "NO" - by clicking "No", the app will be minimized to the taskbar and continue running in the background', icon='warning')
    if response == True:
        stop_observer()
        window.destroy()
    elif response == False:
        msg.showinfo('Minimizing window','This window will now be minimized to the taskbar and continue running in the background')
        window.iconify()

def open_window():
    global b1
    window.title("Filesystem Monitoring")
    app_width = 400
    app_height = 300
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    b1 = tk.Button(window, text="Start monitoring", command=start_observer, fg="green", cursor="hand2")
    b2 = tk.Button(window, text="Stop monitoring", command=stop_observer, fg="red", cursor="hand2")
    b1.place(relx = 0.5, rely = 0.4, anchor = "center")
    b2.place(relx = 0.5, rely = 0.6, anchor = "center")
    window.protocol("WM_DELETE_WINDOW", exit_application)
    window.mainloop()

if __name__ == '__main__':
    add_to_startup(startup_path, start_file_on_login_path)
    open_window()
