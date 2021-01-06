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
# Use "pip3 install watchdog" to install the watchdog library 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# NOTE: GENERAL FOLDER NAMING CONVENTION:
### NOTE -- Ensure to include "2 (TWO)" backslash in ALL PATHS BELOW 
### NOTE -- e.g "C:\Users\explo\Desktop" should be "C:\\Users\\explo\\Desktop"

# Include directory or directories you want to moitor within double quotes and square brackets: directories_to_watch = ["your_dir"]
# Seperate Multiple directories with comma ',' e.g directories_to_watch = ["C:\\your_dir_1", "F:\\your_dir_2"]
directories_to_watch = ["C:\\your_dir_1", "C:\\your_dir_2", "F:\\your_dir_3", "F:\\your_dir_4"]
path_to_write = "C:\\your_dir_5" # Ensure this path is not included in watched directory above
file_name = "filesystem_monitoring.txt" # The filename you want to use to store the event log
storage_path = path_to_write + '\\' + file_name
# Replace path to this "main.py" file with your systems path to "main.py" to start program when you Login
start_file_on_login_path = "C:\\Users\\username\\path_to_main.py_file_on_your_pc\\filesystem_monitoring\\src\\main.py"
# Replace with your startup folder path -> press WinKey + R, then type shell:startup and hit enter to get path.
startup_path = 'C:\\Users\\username\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'

def check_path_exists(path):
    """ This function simply checks that the paths provided exists. 
    If path exists it simply passes else it exits with exit status 1 """
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
    """ A subclass of Watchdog's FileSystemEventHandler class. 
    It listens for the events below and carries out an action
    based on the event that was fired. """
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

# Global button for handling state
b1 = ''
# Initialize event handler
event_handler = Handler()
# Initialize Watchdog's Observer
observer = Observer()
# Initialize Tkinter window
window = tk.Tk()

def add_to_startup(startup_path, file_path):
    """ This function makes program Startup on Login"""
    with open(startup_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(f'python {file_path}')

def dir_watcher(watch_directory):
    """ Schedules an Observer on directories specified in 
    global directories_to_watch list. """
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
    """ Starts an Observer on each directory specified in its own process
    using the multiprocess module and returns process ids for further handling. """
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
    """ Kills all the running processes associated with Observers
    thus, stops all monitoring. """
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
    """ Handles Tkinter default close (X) and Alt + F4 response 
    and returns customized response. """
    response = msg.askyesno('Close Application', f'Are you sure you want to exit the application? \n\n "YES" - by clicking "Yes", the app will close and all observers will be stopped. \n\n "NO" - by clicking "No", the app will be minimized to the taskbar and continue running in the background', icon='warning')
    if response == True:
        stop_observer()
        window.destroy()
    elif response == False:
        msg.showinfo('Minimizing window','This window will now be minimized to the taskbar and continue running in the background')
        window.iconify()

def open_window():
    """ Creates Tkinter window, start and stop buttons, and 
    specifies new protocol for Close (X) window event. """
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
    # Add program to start up
    add_to_startup(startup_path, start_file_on_login_path)
    # Open Tkinter window / Run program
    open_window()
