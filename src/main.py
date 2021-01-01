#!/usr/bin/env python3

import os, sys
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

def dir_watcher(watch_directory):
    observer.schedule(event_handler, watch_directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        print(f"[+] Saved output to {path_to_write}\{file_name}")
        print("[-] Stopped Observer and Caught Exception.")
    observer.join()

def stop_observer():
    observer.stop()
    observer.join()
    sys.exit()


if __name__ == '__main__':
    for watch_directory in directories_to_watch:
        if not os.path.exists(watch_directory.strip(' ')):
            print(f"The Directory/Path {watch_directory} does not exist")
            sys.exit(1)
        mp = multiprocessing.Process(target=dir_watcher, args=(watch_directory.strip(' '),))
        mp.start()
