#!/usr/bin/env python3

import tkinter
from tkinter import messagebox as msg
import os, sys
import signal
import time
import multiprocessing
# Use pip3 install watchdog to install watchdog 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


directories_to_watch = ["C:\\Users\\explo\\Documents", "C:\\xampp\\htdocs", "F:\\laravel-apps", "F:\\All Courses Mike"]
path_to_write = "C:\\Users\\explo\\Desktop"
file_name = "filesystem_monitoring.txt"
storage_path = path_to_write + '\\' + file_name

if not os.path.exists(path_to_write):
    print("The Path does not exist")
    sys.exit(1)

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # Take any action here when a file is first created.
        with open(storage_path, 'a') as file:
            file.write(f"[++] Created {event.src_path}")
            file.write("\n")
    def on_deleted(self, event):
        # Take any action here when a file is first deleted.
        with open(storage_path, 'a') as file:
            file.write(f"[!!] Deleted {event.src_path}")
            file.write("\n")
    def on_moved(self, event):
        # Take any action here when a file is first moved (Renamed).
        with open(storage_path, 'a') as file:
            file.write(f"[>>] Renamed {event.src_path} to {event.dest_path}")
            file.write("\n")

event_handler = Handler()
observer = Observer()
window = tkinter.Tk()

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
    global process_ids
    msg.showinfo('Starting Observer', 'Monitoring will begin in the background if path(s) exist')
    for watch_directory in directories_to_watch:
        if not os.path.exists(watch_directory.strip(' ')):
            msg.showerror('Path Error!', f"The Directory or Path {watch_directory} does not exist. Restart program after fixing path.")
            break
        mp = multiprocessing.Process(target=dir_watcher, args=(watch_directory.strip(' '),))
        mp.start()
        process_ids.append(mp.pid)

def stop_observer():
    global process_ids
    for kill_id in process_ids:
        os.kill(kill_id, signal.SIGINT)
    process_ids = []
    msg.showinfo('Stopping Observer', f"[+] All Observers have been stopped. Saved output to {path_to_write}\{file_name}")

def open_window():
    window.title("Filesystem Monitoring")
    app_width = 400
    app_height = 300
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    b1 = tkinter.Button(window, text="Start monitoring", command=start_observer, fg="green")
    b2 = tkinter.Button(window, text="Stop monitoring", command=stop_observer, fg="red")
    b1.place(relx = 0.5, rely = 0.4, anchor = "center")
    b2.place(relx = 0.5, rely = 0.6, anchor = "center")
    window.mainloop()

if __name__ == '__main__':
    open_window()
